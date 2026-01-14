"""Report generator - creates HTML reports with visualizations"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path


class ReportGenerator:
    def __init__(self, metrics, insights):
        self.metrics = metrics
        self.insights = insights

    def generate(self, output_path):
        """Generate HTML report"""
        Path(output_path).parent.mkdir(exist_ok=True)
        
        html = self._build_html()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

    def _build_html(self):
        """Build complete HTML report"""
        charts = [
            self._chart_loc_trend(),
            self._chart_churn(),
            self._chart_hotspots(),
            self._chart_density()
        ]
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Software Archaeology Report</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ margin: 0 0 10px 0; color: #333; }}
        .summary {{ 
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-top: 15px;
        }}
        .summary-item {{
            margin: 8px 0;
            font-size: 14px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .insights {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .insight-section {{
            margin: 20px 0;
        }}
        .insight-section h3 {{
            color: #555;
            margin-bottom: 10px;
        }}
        .insight-item {{
            background: #f8f9fa;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Software Archaeology Report</h1>
        <p style="color: #666; margin: 5px 0;">Codebase Evolution Analysis</p>
        <div class="summary">
            {''.join(f'<div class="summary-item">{item}</div>' for item in self.insights['summary'])}
        </div>
    </div>

    {self._render_insights()}

    <div class="chart-container">
        <h2>Lines of Code Over Time</h2>
        <div id="loc-chart"></div>
    </div>

    <div class="chart-container">
        <h2>Weekly Code Churn</h2>
        <div id="churn-chart"></div>
    </div>

    <div class="chart-container">
        <h2>Top 20 Hotspots</h2>
        <div id="hotspot-chart"></div>
    </div>

    <div class="chart-container">
        <h2>Commit Density (7-day rolling average)</h2>
        <div id="density-chart"></div>
    </div>

    <script>
        {charts[0]}
        {charts[1]}
        {charts[2]}
        {charts[3]}
    </script>
</body>
</html>
"""
        return html

    def _render_insights(self):
        """Render insights section"""
        html = '<div class="insights"><h2>Key Findings</h2>'
        
        # Instability periods
        if self.insights['instability_periods']:
            html += '<div class="insight-section"><h3>⚠ Instability Periods</h3>'
            for period in self.insights['instability_periods'][:5]:
                html += f'<div class="insight-item">Week {period["week"]}: {period["multiplier"]}× normal churn</div>'
            html += '</div>'
        
        # Risky files
        if self.insights['risky_files']:
            html += '<div class="insight-section"><h3>🔥 High-Risk Files</h3>'
            for file in self.insights['risky_files'][:5]:
                html += f'<div class="insight-item">{file["file"]} (score: {file["score"]}, {file["commits"]} commits)</div>'
            html += '</div>'
        
        # Coupling
        if self.insights['coupling_warnings']:
            html += '<div class="insight-section"><h3>🔗 Temporal Coupling</h3>'
            for warning in self.insights['coupling_warnings']:
                html += f'<div class="insight-item">{warning["file1"]} ↔ {warning["file2"]} (coupling: {warning["coupling"]})</div>'
            html += '</div>'
        
        html += '</div>'
        return html

    def _chart_loc_trend(self):
        """Generate LOC trend chart"""
        data = self.metrics['loc_over_time']
        
        # Sample data if too many points
        if len(data) > 500:
            step = len(data) // 500
            data = data[::step]
        
        dates = [d['date'] for d in data]
        loc = [d['loc'] for d in data]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=loc,
            mode='lines',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Lines of Code',
            hovermode='x unified',
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        return f"Plotly.newPlot('loc-chart', {fig.to_json()});"

    def _chart_churn(self):
        """Generate churn chart"""
        data = self.metrics['weekly_churn']
        
        weeks = [d['week'] for d in data]
        churn = [d['churn'] for d in data]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weeks, y=churn,
            marker_color='#ff7f0e'
        ))
        
        # Add median line
        if churn:
            import statistics
            median = statistics.median(churn)
            fig.add_hline(y=median, line_dash="dash", line_color="red",
                         annotation_text=f"Median: {median:.0f}")
        
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Lines Changed (Added + Deleted)',
            hovermode='x unified',
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        return f"Plotly.newPlot('churn-chart', {fig.to_json()});"

    def _chart_hotspots(self):
        """Generate hotspot chart"""
        data = self.metrics['hotspots'][:20]
        
        files = [d['file'].split('/')[-1] if '/' in d['file'] else d['file'] for d in data]
        scores = [d['score'] for d in data]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=files[::-1],  # Reverse for top-to-bottom
            x=scores[::-1],
            orientation='h',
            marker=dict(
                color=scores[::-1],
                colorscale='Reds',
                showscale=True
            )
        ))
        
        fig.update_layout(
            xaxis_title='Hotspot Score',
            yaxis_title='File',
            height=600,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        return f"Plotly.newPlot('hotspot-chart', {fig.to_json()});"

    def _chart_density(self):
        """Generate commit density chart"""
        data = self.metrics['commit_density']
        
        # Sample if too many points
        if len(data) > 500:
            step = len(data) // 500
            data = data[::step]
        
        dates = [d['date'] for d in data]
        density = [d['density'] for d in data]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=density,
            mode='lines',
            line=dict(color='#2ca02c', width=1),
            fill='tozeroy',
            fillcolor='rgba(44, 160, 44, 0.2)'
        ))
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Commits per Day (7-day avg)',
            hovermode='x unified',
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        return f"Plotly.newPlot('density-chart', {fig.to_json()});"
