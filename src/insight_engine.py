"""Insight engine - generates actionable insights from metrics"""

import statistics
import re


class InsightEngine:
    def __init__(self, metrics):
        self.metrics = metrics

    def analyze(self):
        """Generate all insights"""
        insights = {
            'instability_periods': self._detect_instability(),
            'risky_files': self._identify_risky_files(),
            'bug_fix_correlation': self._analyze_bug_fixes(),
            'stagnation': self._detect_stagnation(),
            'coupling_warnings': self._analyze_coupling(),
            'summary': []
        }
        
        # Generate summary
        insights['summary'] = self._generate_summary(insights)
        
        return insights

    def _detect_instability(self):
        """Detect periods of high churn"""
        weekly_churn = self.metrics['weekly_churn']
        
        if len(weekly_churn) < 4:
            return []
        
        churn_values = [w['churn'] for w in weekly_churn]
        median_churn = statistics.median(churn_values)
        
        threshold = median_churn * 2
        
        unstable_periods = []
        for week_data in weekly_churn:
            if week_data['churn'] > threshold:
                unstable_periods.append({
                    'week': week_data['week'],
                    'churn': week_data['churn'],
                    'multiplier': round(week_data['churn'] / median_churn, 1)
                })
        
        return unstable_periods

    def _identify_risky_files(self):
        """Identify high-risk files"""
        hotspots = self.metrics['hotspots']
        
        if not hotspots:
            return []
        
        # Top 10% or top 10 files, whichever is smaller
        threshold_count = max(min(len(hotspots) // 10, 10), 3)
        
        risky = hotspots[:threshold_count]
        
        return [{
            'file': h['file'],
            'score': round(h['score'], 2),
            'commits': h['commits'],
            'churn': h['churn']
        } for h in risky]

    def _analyze_bug_fixes(self):
        """Analyze bug-fix patterns (placeholder - needs commit messages)"""
        # This would require analyzing commit messages from the database
        # For MVP, return placeholder
        return {
            'detected': False,
            'note': 'Bug-fix analysis requires commit message parsing (future enhancement)'
        }

    def _detect_stagnation(self):
        """Detect if codebase is stagnant"""
        halflife = self.metrics.get('stability_halflife')
        
        if not halflife:
            return {'stagnant': False}
        
        days = halflife['days']
        
        if days > 180:
            return {
                'stagnant': True,
                'halflife_days': days,
                'message': f"50% of files unchanged in {days:.0f} days - possible stagnation"
            }
        
        return {
            'stagnant': False,
            'halflife_days': days
        }

    def _analyze_coupling(self):
        """Analyze temporal coupling warnings"""
        coupling = self.metrics['temporal_coupling']
        
        warnings = []
        for pair in coupling[:5]:  # Top 5 coupled pairs
            if pair['score'] > 0.5:
                warnings.append({
                    'file1': pair['file1'],
                    'file2': pair['file2'],
                    'coupling': round(pair['score'], 2),
                    'recommendation': 'Consider refactoring - high behavioral coupling'
                })
        
        return warnings

    def _generate_summary(self, insights):
        """Generate human-readable summary"""
        summary = []
        
        # Metadata
        meta = self.metrics['metadata']
        summary.append(f"Analyzed {meta['total_commits']} commits across {meta['total_files']} files")
        summary.append(f"Period: {meta['start_date'][:10]} to {meta['end_date'][:10]}")
        
        # Instability
        if insights['instability_periods']:
            count = len(insights['instability_periods'])
            summary.append(f"⚠ {count} instability period(s) detected with >2× normal churn")
        
        # Risky files
        if insights['risky_files']:
            top_file = insights['risky_files'][0]
            summary.append(f"🔥 Top hotspot: {top_file['file']} (score: {top_file['score']})")
        
        # Coupling
        if insights['coupling_warnings']:
            summary.append(f"🔗 {len(insights['coupling_warnings'])} high-coupling file pairs detected")
        
        # Stagnation
        if insights['stagnation'].get('stagnant'):
            summary.append(f"⏸ Possible stagnation detected")
        elif 'halflife_days' in insights['stagnation']:
            days = insights['stagnation']['halflife_days']
            summary.append(f"✓ Active codebase (half-life: {days:.0f} days)")
        
        return summary
