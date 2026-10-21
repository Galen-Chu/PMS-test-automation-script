"""Performance data analyzer: segment rounds, compute statistics, check thresholds.

Takes raw performance data (from PerformanceMonitor) and produces
structured analysis with per-round metrics, medians, and threshold checks.
"""

import json
import statistics
from typing import Any


def segment_rounds(ops: list, apis: list, save_api_pattern: str = "booking") -> list:
    """Segment operations and API calls into rounds based on save API completion.

    A "round" starts when the first API fires and ends when a save API
    (matching save_api_pattern) completes.

    Args:
        ops: list of click/input events with 't' (ms since page load)
        apis: list of API entries with 'start', 'duration', 'name'
        save_api_pattern: pattern to identify the save API (default: "booking")

    Returns:
        list of round dicts, each containing:
        - ops: operations within this round
        - apis: API calls within this round
        - save_api: the save API entry (if found)
        - save_duration_ms: save API duration
        - recalc_duration_ms: recalculate API duration (if found)
    """
    if not apis:
        return []

    # Find save API boundaries
    save_apis = sorted(
        [a for a in apis if save_api_pattern in a.get("name", "")],
        key=lambda x: x["start"] + x["duration"],
    )

    rounds = []
    boundary = 0  # ms timestamp of previous round's end

    for save in save_apis:
        round_end = save["start"] + save["duration"]
        round_apis = [a for a in apis if boundary <= a["start"] < round_end]
        round_ops = [o for o in ops if boundary <= o.get("t", 0) < round_end]

        # Find recalculate API
        recalc = None
        for a in round_apis:
            name = a.get("name", "")
            if "recalculate" in name or "rent-price" in name:
                if a["duration"] > 1000:  # Slow recalcs only
                    recalc = a
                    break

        rounds.append(
            {
                "ops": round_ops,
                "apis": round_apis,
                "save_api": save,
                "save_duration_ms": save["duration"],
                "recalc_duration_ms": recalc["duration"] if recalc else None,
                "recalc_api": recalc,
            }
        )
        boundary = round_end

    # Any trailing APIs after the last save
    trailing = [a for a in apis if a["start"] >= boundary]
    if trailing:
        rounds.append(
            {
                "ops": [o for o in ops if o.get("t", 0) >= boundary],
                "apis": trailing,
                "save_api": None,
                "save_duration_ms": None,
                "recalc_duration_ms": None,
                "recalc_api": None,
            }
        )

    return rounds


def compute_stats(values: list) -> dict:
    """Compute median, min, max, and count for a list of values."""
    if not values:
        return {"count": 0, "median": None, "min": None, "max": None, "mean": None}
    return {
        "count": len(values),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
        "mean": statistics.mean(values),
    }


def analyze_performance(perf_data: dict, thresholds: dict | None = None) -> dict:
    """Full performance analysis from raw data.

    Args:
        perf_data: dict with 'ops' and 'apis' from PerformanceMonitor.stop()
        thresholds: optional dict of {api_pattern: max_duration_ms}

    Returns:
        dict with rounds, stats, slow_apis, violations
    """
    ops = perf_data.get("ops", [])
    apis = perf_data.get("apis", [])

    # Segment into rounds
    rounds = segment_rounds(ops, apis)

    # Compute stats per metric
    save_durations = [r["save_duration_ms"] for r in rounds if r["save_duration_ms"]]
    recalc_durations = [r["recalc_duration_ms"] for r in rounds if r["recalc_duration_ms"]]

    stats = {
        "save": compute_stats(save_durations),
        "recalculate": compute_stats(recalc_durations),
        "total_api_count": len(apis),
        "round_count": len(rounds),
    }

    # Top 10 slowest APIs
    sorted_apis = sorted(apis, key=lambda x: x["duration"], reverse=True)
    slow_apis = sorted_apis[:10]

    # Threshold violations
    violations = []
    if thresholds:
        for api in apis:
            for pattern, limit in thresholds.items():
                if pattern in api.get("name", "") and api["duration"] > limit:
                    violations.append(
                        {
                            "api": api["name"],
                            "duration_ms": api["duration"],
                            "threshold_ms": limit,
                            "exceeded_by_ms": api["duration"] - limit,
                        }
                    )

    return {
        "rounds": rounds,
        "stats": stats,
        "slow_apis": slow_apis,
        "violations": violations,
    }


def format_duration(ms: float | None) -> str:
    """Format milliseconds as human-readable string."""
    if ms is None:
        return "N/A"
    if ms < 1000:
        return f"{ms:.0f}ms"
    return f"{ms / 1000:.2f}s"
