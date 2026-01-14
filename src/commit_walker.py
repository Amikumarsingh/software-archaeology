"""Commit walker - extracts commit history and file changes"""

import sqlite3
import pygit2
from pathlib import Path
from datetime import datetime


class CommitWalker:
    def __init__(self, repo, sample_rate=None):
        self.repo = repo
        self.sample_rate = sample_rate
        self.db_path = Path('data/repo_data.db')

    def extract_to_db(self):
        """Walk commits and extract to SQLite database"""
        self.db_path.parent.mkdir(exist_ok=True)
        if self.db_path.exists():
            self.db_path.unlink()

        conn = sqlite3.connect(self.db_path)
        self._create_schema(conn)

        commit_count = 0
        batch = []

        # Walk commits in topological order
        for commit in self.repo.walk(self.repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL):
            if self.sample_rate and commit_count % self.sample_rate != 0:
                commit_count += 1
                continue

            batch.append(self._extract_commit(commit))
            
            if len(batch) >= 1000:
                self._write_batch(conn, batch)
                batch = []
                print(f"   Processed {commit_count} commits...", end='\r')

            commit_count += 1

        if batch:
            self._write_batch(conn, batch)

        conn.commit()
        conn.close()
        print(f"   Processed {commit_count} commits total")
        return self.db_path

    def _create_schema(self, conn):
        """Create database schema"""
        conn.execute('''
            CREATE TABLE commits (
                sha TEXT PRIMARY KEY,
                timestamp INTEGER,
                author TEXT,
                message TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE file_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commit_sha TEXT,
                file_path TEXT,
                lines_added INTEGER,
                lines_deleted INTEGER,
                FOREIGN KEY (commit_sha) REFERENCES commits(sha)
            )
        ''')
        conn.execute('CREATE INDEX idx_file_path ON file_changes(file_path)')
        conn.execute('CREATE INDEX idx_commit_sha ON file_changes(commit_sha)')

    def _extract_commit(self, commit):
        """Extract commit metadata and file changes"""
        timestamp = commit.commit_time
        author = commit.author.name
        message = commit.message.strip()
        
        file_changes = []
        
        # Get diff against first parent (or empty tree for initial commit)
        if commit.parents:
            parent = commit.parents[0]
            diff = self.repo.diff(parent, commit, context_lines=0)
        else:
            diff = commit.tree.diff_to_tree(context_lines=0, swap=True)

        # Find renames
        diff.find_similar(flags=pygit2.GIT_DIFF_FIND_RENAMES)

        for patch in diff:
            delta = patch.delta
            file_path = delta.new_file.path
            
            # Skip binary files
            if delta.is_binary:
                continue

            lines_added = patch.line_stats[1]
            lines_deleted = patch.line_stats[2]
            
            file_changes.append((file_path, lines_added, lines_deleted))

        return (str(commit.id), timestamp, author, message, file_changes)

    def _write_batch(self, conn, batch):
        """Write batch of commits to database"""
        for sha, timestamp, author, message, file_changes in batch:
            conn.execute(
                'INSERT INTO commits VALUES (?, ?, ?, ?)',
                (sha, timestamp, author, message)
            )
            
            for file_path, added, deleted in file_changes:
                conn.execute(
                    'INSERT INTO file_changes (commit_sha, file_path, lines_added, lines_deleted) VALUES (?, ?, ?, ?)',
                    (sha, file_path, added, deleted)
                )
