"""Metrics calculator - computes evolution metrics"""

import sqlite3
import json
from datetime import datetime, timedelta
from collections import defaultdict
import math


class MetricsCalculator:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def compute_all(self):
        """Compute all metrics and return as dictionary"""
        metrics = {
            'metadata': self._get_metadata(),
            'loc_over_time': self._compute_loc_trend(),
            'weekly_churn': self._compute_churn(),
            'file_volatility': self._compute_volatility(),
            'commit_density': self._compute_density(),
            'hotspots': self._compute_hotspots(),
            'temporal_coupling': self._compute_coupling(),
            'stability_halflife': self._compute_halflife()
        }
        
        # Save to JSON
        output_path = 'data/metrics.json'
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        return metrics

    def _get_metadata(self):
        """Get repository metadata"""
        cursor = self.conn.execute('SELECT COUNT(*) FROM commits')
        total_commits = cursor.fetchone()[0]
        
        cursor = self.conn.execute('SELECT MIN(timestamp), MAX(timestamp) FROM commits')
        min_ts, max_ts = cursor.fetchone()
        
        cursor = self.conn.execute('SELECT COUNT(DISTINCT file_path) FROM file_changes')
        total_files = cursor.fetchone()[0]
        
        return {
            'total_commits': total_commits,
            'start_date': datetime.fromtimestamp(min_ts).isoformat(),
            'end_date': datetime.fromtimestamp(max_ts).isoformat(),
            'total_files': total_files
        }

    def _compute_loc_trend(self):
        """Compute cumulative LOC over time"""
        cursor = self.conn.execute('''
            SELECT c.timestamp, SUM(fc.lines_added - fc.lines_deleted) as net_change
            FROM commits c
            JOIN file_changes fc ON c.sha = fc.commit_sha
            GROUP BY c.sha
            ORDER BY c.timestamp
        ''')
        
        cumulative_loc = 0
        trend = []
        
        for timestamp, net_change in cursor:
            cumulative_loc += net_change
            trend.append({
                'date': datetime.fromtimestamp(timestamp).isoformat(),
                'loc': max(0, cumulative_loc)  # Prevent negative LOC
            })
        
        return trend

    def _compute_churn(self):
        """Compute weekly code churn"""
        cursor = self.conn.execute('''
            SELECT c.timestamp, SUM(fc.lines_added + fc.lines_deleted) as churn
            FROM commits c
            JOIN file_changes fc ON c.sha = fc.commit_sha
            GROUP BY c.sha
            ORDER BY c.timestamp
        ''')
        
        weekly_churn = defaultdict(int)
        
        for timestamp, churn in cursor:
            dt = datetime.fromtimestamp(timestamp)
            week_key = dt.strftime('%Y-W%U')
            weekly_churn[week_key] += churn
        
        return [{'week': k, 'churn': v} for k, v in sorted(weekly_churn.items())]

    def _compute_volatility(self):
        """Compute file volatility (commit frequency)"""
        cursor = self.conn.execute('SELECT COUNT(*) FROM commits')
        total_commits = cursor.fetchone()[0]
        
        cursor = self.conn.execute('''
            SELECT file_path, COUNT(DISTINCT commit_sha) as commit_count
            FROM file_changes
            GROUP BY file_path
        ''')
        
        volatility = []
        for file_path, commit_count in cursor:
            volatility.append({
                'file': file_path,
                'commits': commit_count,
                'volatility': commit_count / total_commits
            })
        
        return sorted(volatility, key=lambda x: x['volatility'], reverse=True)

    def _compute_density(self):
        """Compute daily commit density with 7-day rolling window"""
        cursor = self.conn.execute('SELECT timestamp FROM commits ORDER BY timestamp')
        
        daily_commits = defaultdict(int)
        for (timestamp,) in cursor:
            date = datetime.fromtimestamp(timestamp).date()
            daily_commits[date] += 1
        
        if not daily_commits:
            return []
        
        min_date = min(daily_commits.keys())
        max_date = max(daily_commits.keys())
        
        density = []
        current = min_date
        while current <= max_date:
            # 7-day window
            window_sum = sum(daily_commits.get(current + timedelta(days=i), 0) for i in range(-3, 4))
            density.append({
                'date': current.isoformat(),
                'density': window_sum / 7
            })
            current += timedelta(days=1)
        
        return density

    def _compute_hotspots(self):
        """Compute hotspot scores (volatility × log(churn))"""
        cursor = self.conn.execute('''
            SELECT 
                file_path,
                COUNT(DISTINCT commit_sha) as commits,
                SUM(lines_added + lines_deleted) as total_churn
            FROM file_changes
            GROUP BY file_path
        ''')
        
        total_commits = self.conn.execute('SELECT COUNT(*) FROM commits').fetchone()[0]
        
        hotspots = []
        for file_path, commits, total_churn in cursor:
            volatility = commits / total_commits
            hotspot_score = volatility * math.log(1 + total_churn)
            
            hotspots.append({
                'file': file_path,
                'score': hotspot_score,
                'commits': commits,
                'churn': total_churn
            })
        
        return sorted(hotspots, key=lambda x: x['score'], reverse=True)[:50]

    def _compute_coupling(self):
        """Compute temporal coupling between files"""
        # Get files modified in each commit
        cursor = self.conn.execute('''
            SELECT commit_sha, GROUP_CONCAT(file_path) as files
            FROM file_changes
            GROUP BY commit_sha
        ''')
        
        # Count co-occurrences
        file_commits = defaultdict(set)
        co_occurrences = defaultdict(int)
        
        for commit_sha, files_str in cursor:
            files = files_str.split(',')
            
            for f in files:
                file_commits[f].add(commit_sha)
            
            # Only compute for commits with 2-10 files (avoid noise)
            if 2 <= len(files) <= 10:
                for i, f1 in enumerate(files):
                    for f2 in files[i+1:]:
                        pair = tuple(sorted([f1, f2]))
                        co_occurrences[pair] += 1
        
        # Compute coupling scores
        coupling = []
        for (f1, f2), co_count in co_occurrences.items():
            if co_count < 3:  # Minimum threshold
                continue
            
            f1_count = len(file_commits[f1])
            f2_count = len(file_commits[f2])
            
            if f1_count < 5 or f2_count < 5:  # Filter low-activity files
                continue
            
            coupling_score = co_count / min(f1_count, f2_count)
            
            if coupling_score > 0.3:
                coupling.append({
                    'file1': f1,
                    'file2': f2,
                    'score': coupling_score,
                    'co_changes': co_count
                })
        
        return sorted(coupling, key=lambda x: x['score'], reverse=True)[:20]

    def _compute_halflife(self):
        """Compute stability half-life"""
        cursor = self.conn.execute('''
            SELECT DISTINCT file_path, MAX(c.timestamp) as last_modified
            FROM file_changes fc
            JOIN commits c ON fc.commit_sha = c.sha
            GROUP BY file_path
            ORDER BY last_modified DESC
        ''')
        
        files_by_date = [(f, ts) for f, ts in cursor]
        
        if not files_by_date:
            return None
        
        total_files = len(files_by_date)
        half_count = total_files // 2
        
        if half_count < len(files_by_date):
            halflife_timestamp = files_by_date[half_count][1]
            latest_timestamp = files_by_date[0][1]
            
            days = (latest_timestamp - halflife_timestamp) / 86400
            return {
                'days': round(days, 1),
                'interpretation': self._interpret_halflife(days)
            }
        
        return None

    def _interpret_halflife(self, days):
        """Interpret half-life value"""
        if days < 14:
            return "Very active - rapid development"
        elif days < 60:
            return "Active development"
        elif days < 180:
            return "Moderate activity"
        else:
            return "Stable or stagnant"
