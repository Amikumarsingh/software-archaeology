"""Test script - validates tool on current repository"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.repo_loader import RepoLoader
from src.commit_walker import CommitWalker
from src.metrics_calculator import MetricsCalculator
from src.insight_engine import InsightEngine
from src.report_generator import ReportGenerator


def test_on_self():
    """Test the tool on its own repository"""
    print("Testing Software Archaeology on itself...")
    
    # Use current directory
    repo_path = os.path.dirname(os.path.dirname(__file__))
    
    print(f"\n[1/5] Loading repository: {repo_path}")
    loader = RepoLoader(repo_path)
    repo = loader.load()
    print(f"   [OK] Repository loaded: {repo.workdir}")

    print("\n[2/5] Extracting commit history...")
    walker = CommitWalker(repo)
    db_path = walker.extract_to_db()
    print(f"   [OK] Database created: {db_path}")

    print("\n[3/5] Computing metrics...")
    calculator = MetricsCalculator(db_path)
    metrics = calculator.compute_all()
    print(f"   [OK] Computed metrics for {metrics['metadata']['total_commits']} commits")

    print("\n[4/5] Generating insights...")
    engine = InsightEngine(metrics)
    insights = engine.analyze()
    print(f"   [OK] Generated {len(insights['summary'])} insights")

    print("\n[5/5] Creating report...")
    generator = ReportGenerator(metrics, insights)
    output_path = 'output/self_test_report.html'
    generator.generate(output_path)
    print(f"   [OK] Report saved: {output_path}")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for item in insights['summary']:
        print(f"  {item}")
    print("="*60)
    
    print(f"\n[SUCCESS] Test complete! Open {output_path} in your browser.")


if __name__ == '__main__':
    test_on_self()
