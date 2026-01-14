#!/usr/bin/env python3
"""Software Archaeology - Codebase Time Machine"""

import sys
import argparse
from pathlib import Path
from src.repo_loader import RepoLoader
from src.commit_walker import CommitWalker
from src.metrics_calculator import MetricsCalculator
from src.insight_engine import InsightEngine
from src.report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(description='Analyze Git repository evolution')
    parser.add_argument('repo_path', help='Path to Git repository or URL')
    parser.add_argument('--output', default='output/report.html', help='Output file path')
    parser.add_argument('--sample', type=int, help='Sample every Nth commit (for large repos)')
    args = parser.parse_args()

    print(f"[1/5] Loading repository: {args.repo_path}")
    loader = RepoLoader(args.repo_path)
    repo = loader.load()

    print("[2/5] Extracting commit history...")
    walker = CommitWalker(repo, sample_rate=args.sample)
    db_path = walker.extract_to_db()

    print("[3/5] Computing metrics...")
    calculator = MetricsCalculator(db_path)
    metrics = calculator.compute_all()

    print("[4/5] Generating insights...")
    engine = InsightEngine(metrics)
    insights = engine.analyze()

    print("[5/5] Creating report...")
    generator = ReportGenerator(metrics, insights)
    generator.generate(args.output)

    print(f"\n[SUCCESS] Analysis complete: {args.output}")


if __name__ == '__main__':
    main()
