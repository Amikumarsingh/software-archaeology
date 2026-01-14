# Software Archaeology: Codebase Time Machine

> Analyze how your codebase evolves over time, identify volatility hotspots, and surface signals of technical debt.

🔗 **[Live Demo](https://amikumarsingh.github.io/software-archaeology/)** | 📊 **[Example Report](https://amikumarsingh.github.io/software-archaeology/demo_report.html)**

## The Problem

Every codebase has a history, but we rarely examine it systematically. We review code at a point in time, but ignore the story of how it evolved.

**Key questions this tool answers:**
- Which parts of our codebase are unstable?
- When did we introduce technical debt?
- Are there hidden dependencies between files?
- Is our codebase healthy or stagnant?

## Why This Matters

1. **Risk Management**: Identify high-churn files before they cause outages
2. **Refactoring Prioritization**: Focus efforts on volatile, coupled code
3. **Team Onboarding**: New engineers see which files are "hot" vs. stable
4. **Post-Mortem Analysis**: Correlate incidents with code churn patterns
5. **Technical Debt Visibility**: Quantify instability, not just "code smells"

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Analyze a local repository
```bash
python archaeology.py /path/to/repo --output report.html
```

### Analyze a remote repository
```bash
python archaeology.py https://github.com/facebook/react --output react_report.html
```

### For large repositories (sample every 10th commit)
```bash
python archaeology.py https://github.com/torvalds/linux --sample 10 --output linux_report.html
```

## Metrics Explained

### Core Metrics

1. **Lines of Code Over Time**: Shows growth trajectory; sudden drops indicate deletions/refactors
2. **Code Churn**: Lines added + deleted per week (measures activity and instability)
3. **File Volatility**: Commit frequency per file (identifies change hotspots)
4. **Commit Density**: Commits per day with 7-day smoothing (reveals development rhythm)
5. **Hotspot Score**: Volatility × log(churn) — identifies files that change frequently AND substantially

### Advanced Metrics

6. **Temporal Coupling**: How often file pairs change together (finds hidden dependencies)
7. **Stability Half-Life**: Time window covering 50% of recent changes (quantifies codebase freshness)

## Example Insights

**From analyzing React:**
> "Instability spike detected in March 2017 (3.2× normal churn), corresponding to the Fiber architecture rewrite. Top hotspot: ReactFiberWorkLoop.js (modified in 847 commits)."

**From analyzing a typical project:**
> "High temporal coupling detected between UserService.java ↔ UserRepository.java (0.67). These files change together 67% of the time—consider clarifying interface boundaries."

## Output

The tool generates:
- **HTML Report**: Interactive visualizations with Plotly
- **JSON Data**: Raw metrics in `data/metrics.json`
- **SQLite Database**: Commit history in `data/repo_data.db`

## Architecture

```
Repository → Extract Commits → Compute Metrics → Generate Insights → Visualize
```

**Modules:**
- `RepoLoader`: Clone or open Git repositories
- `CommitWalker`: Extract commit history to SQLite
- `MetricsCalculator`: Compute all evolution metrics
- `InsightEngine`: Apply heuristics to detect patterns
- `ReportGenerator`: Create HTML reports with charts

## Limitations

1. **No semantic analysis**: We don't parse code, only diffs
2. **Rename detection**: Imperfect for files with heavy edits (>50% change)
3. **Language-agnostic**: Doesn't account for language-specific patterns
4. **Correlation ≠ causation**: Insights are signals, not proof

## Performance

- Small repos (<1K commits): ~10 seconds
- Medium repos (1K-10K commits): ~1-2 minutes
- Large repos (10K-100K commits): ~5-10 minutes
- Very large repos (>100K commits): Use `--sample` flag

## Future Enhancements

- [ ] Incremental updates (don't reprocess entire history)
- [ ] Bug-fix correlation (analyze commit messages)
- [ ] Author patterns (without "blaming")
- [ ] Comparative analysis (compare branches or time periods)
- [ ] Language-aware LOC (integrate tokei/cloc)
- [ ] IDE integration (show hotspot scores in editor)

## Research Background

This tool synthesizes ideas from:
- **"Your Code as a Crime Scene"** (Adam Tornhill) – Hotspot analysis
- **Software evolution research** (Lehman's laws)
- **Mining software repositories** (MSR) – Temporal coupling

## License

MIT

## Contributing

This is a research-oriented engineering project. Contributions welcome!

Focus areas:
- Performance optimization for very large repos
- Additional metrics with clear justification
- Validation on diverse codebases
- Improved heuristics for insight generation
