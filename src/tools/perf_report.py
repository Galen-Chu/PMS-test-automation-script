"""HTML performance report generator.

Produces a standalone HTML report from performance test analysis data.
Designed for both pytest (via conftest hook) and standalone usage.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from tools.perf_analyzer import format_duration

REPORT_STYLE = """
<style>
  body { font-family: system-ui, -apple-system, sans-serif; margin: 20px; background: #f9f9f7; color: #0b0b0b; }
  .card { background: #fcfcfb; border: 1px solid #e1e0d9; border-radius: 8px; padding: 16px; margin: 16px 0; }
  h1 { font-size: 22px; margin: 0; }
  h2 { font-size: 16px; margin: 10px 0; }
  table { border-collapse: collapse; width: 100%; font-size: 13px; }
  th, td { padding: 6px 10px; text-align: left; border-bottom: 1px solid #e1e0d9; }
  th { color: #52514e; font-weight: 600; font-size: 12px; }
  .stat { font-size: 28px; font-weight: 650; }
  .label { font-size: 12px; color: #898781; }
  .violation { color: #d03b3b; font-weight: 600; }
  .pass { color: #0ca30c; font-weight: 600; }
  .sub { font-size: 12px; color: #52514e; line-height: 1.5; }
</style>
"""


def generate_html_report(analysis: dict, metadata: dict | None = None) -> str:
    """Generate standalone HTML report from analysis data.

    Args:
        analysis: dict from perf_analyzer.analyze_performance()
        metadata: optional dict with test_env, test_date, etc.

    Returns:
        HTML string
    """
    meta = metadata or {}
    stats = analysis.get("stats", {})
    save_stats = stats.get("save", {})
    recalc_stats = stats.get("recalculate", {})

    html_parts = [
        "<!DOCTYPE html><html><head><meta charset='UTF-8'>",
        f"<title>Performance Report</title>{REPORT_STYLE}</head><body>",
        f"<h1>Performance Test Report</h1>",
        f"<div class='sub'>",
        f"  Environment: {meta.get('env', 'N/A')} | ",
        f"Date: {meta.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))}",
        f"</div>",
    ]

    # Summary cards
    html_parts.append("<div style='display:flex;gap:12px;flex-wrap:wrap'>")
    html_parts.append(_stat_card("Save API Median", format_duration(save_stats.get("median"))))
    html_parts.append(_stat_card("Save API Max", format_duration(save_stats.get("max"))))
    html_parts.append(_stat_card("Rounds", str(stats.get("round_count", 0))))
    html_parts.append(
        _stat_card(
            "Threshold",
            "PASS" if not analysis.get("violations") else "FAIL",
            "pass" if not analysis.get("violations") else "violation",
        )
    )
    html_parts.append("</div>")

    # Round details table
    html_parts.append("<div class='card'><h2>Round Details</h2>")
    html_parts.append("<table><tr><th>Round</th><th>Save API</th><th>Recalculate</th></tr>")
    for i, round_data in enumerate(analysis.get("rounds", [])):
        save_ms = round_data.get("save_duration_ms")
        recalc_ms = round_data.get("recalc_duration_ms")
        html_parts.append(
            f"<tr><td>{i + 1}</td>"
            f"<td>{format_duration(save_ms)}</td>"
            f"<td>{format_duration(recalc_ms)}</td></tr>"
        )
    html_parts.append("</table></div>")

    # Statistics table
    html_parts.append("<div class='card'><h2>Statistics</h2>")
    html_parts.append(
        "<table><tr><th>Metric</th><th>Count</th><th>Median</th>" "<th>Min</th><th>Max</th></tr>"
    )
    html_parts.append(
        f"<tr><td>Save API</td><td>{save_stats.get('count', 0)}</td>"
        f"<td><b>{format_duration(save_stats.get('median'))}</b></td>"
        f"<td>{format_duration(save_stats.get('min'))}</td>"
        f"<td>{format_duration(save_stats.get('max'))}</td></tr>"
    )
    if recalc_stats.get("count"):
        html_parts.append(
            f"<tr><td>Recalculate</td><td>{recalc_stats.get('count', 0)}</td>"
            f"<td><b>{format_duration(recalc_stats.get('median'))}</b></td>"
            f"<td>{format_duration(recalc_stats.get('min'))}</td>"
            f"<td>{format_duration(recalc_stats.get('max'))}</td></tr>"
        )
    html_parts.append("</table></div>")

    # Top 10 slowest APIs
    html_parts.append("<div class='card'><h2>Top 10 Slowest APIs</h2>")
    html_parts.append("<table><tr><th>Duration</th><th>API</th></tr>")
    for api in analysis.get("slow_apis", []):
        duration = api.get("duration", 0)
        color = " style='color:#d03b3b'" if duration > 10000 else ""
        html_parts.append(
            f"<tr><td{color}>{format_duration(duration)}</td>"
            f"<td>{api.get('name', 'N/A')}</td></tr>"
        )
    html_parts.append("</table></div>")

    # Violations
    violations = analysis.get("violations", [])
    if violations:
        html_parts.append("<div class='card'><h2>Threshold Violations</h2>")
        html_parts.append(
            "<table><tr><th>API</th><th>Duration</th><th>Threshold</th>" "<th>Exceeded By</th></tr>"
        )
        for v in violations:
            html_parts.append(
                f"<tr class='violation'>"
                f"<td>{v['api']}</td>"
                f"<td>{format_duration(v['duration_ms'])}</td>"
                f"<td>{format_duration(v['threshold_ms'])}</td>"
                f"<td>{format_duration(v['exceeded_by_ms'])}</td></tr>"
            )
        html_parts.append("</table></div>")

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def _stat_card(label: str, value: str, css_class: str = "") -> str:
    """Generate a stat card HTML snippet."""
    cls = f" {css_class}" if css_class else ""
    return (
        f"<div class='card' style='min-width:150px'>"
        f"<div class='label'>{label}</div>"
        f"<div class='stat{cls}'>{value}</div>"
        f"</div>"
    )


def save_report(analysis: dict, output_path: str, metadata: dict | None = None):
    """Generate and save HTML report to file."""
    html = generate_html_report(analysis, metadata)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"Report saved: {output_path}")
