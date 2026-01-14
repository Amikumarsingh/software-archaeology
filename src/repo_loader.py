"""Repository loader - handles cloning and opening Git repositories"""

import pygit2
from pathlib import Path
import tempfile
import shutil


class RepoLoader:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.temp_dir = None

    def load(self):
        """Load repository from path or URL"""
        if self._is_url(self.repo_path):
            return self._clone_repo()
        else:
            return self._open_local()

    def _is_url(self, path):
        return path.startswith('http://') or path.startswith('https://') or path.startswith('git@')

    def _clone_repo(self):
        """Clone remote repository to temp directory"""
        self.temp_dir = tempfile.mkdtemp(prefix='archaeology_')
        print(f"   Cloning to {self.temp_dir}...")
        repo = pygit2.clone_repository(self.repo_path, self.temp_dir)
        return repo

    def _open_local(self):
        """Open local repository"""
        path = Path(self.repo_path).resolve()
        if not path.exists():
            raise ValueError(f"Repository not found: {path}")
        return pygit2.Repository(str(path))

    def cleanup(self):
        """Remove temporary clone if created"""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
