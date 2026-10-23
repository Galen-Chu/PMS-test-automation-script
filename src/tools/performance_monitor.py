"""Performance monitoring utility for Selenium tests.

Injects click/input listeners and Performance Resource Timing capture
into the browser, enabling per-test API timing measurement without
changing existing test logic.

Usage:
    # In test:
    def test_something(self, logged_in_driver, perf_monitor):
        perf_monitor.start()
        # ... existing page operations ...
        perf_monitor.stop()
        perf_monitor.attach_to_allure("my_test")

    # Or with context manager:
    with perf_monitor.measure("save_operation"):
        page.click_save_button()
"""

import json
import time
from pathlib import Path

# JavaScript injected into the page for click/input tracking + resource timing
_HOOK_JS = """
if (!window.__perf_hook_installed) {
window.__perf_hook_installed = true;
window.__perf_ops = [];
window.addEventListener('click', function(e) {
    var t = e.target;
    var parts = [];
    if (t.id) parts.push('#' + t.id);
    if (t.placeholder) parts.push('ph=' + t.placeholder);
    var txt = (t.innerText || t.value || '').trim().slice(0, 30);
    if (txt) parts.push('"' + txt + '"');
    parts.push(t.tagName.toLowerCase());
    window.__perf_ops.push({
        t: performance.now(),
        type: 'click',
        desc: parts.join(' ')
    });
}, true);

window.addEventListener('input', function(e) {
    var t = e.target;
    if (t.tagName === 'INPUT') {
        window.__perf_ops.push({
            t: performance.now(),
            type: 'input',
            desc: (t.placeholder || t.className || '').slice(0, 30) + '=' + String(e.data || '').slice(0, 10)
        });
    }
}, true);
}
"""

_DUMP_JS = """
(function() {
    var ops = window.__perf_ops || [];
    var resources = performance.getEntriesByType('resource')
        .filter(function(e) {
            return e.initiatorType === 'xmlhttprequest' || e.initiatorType === 'fetch';
        })
        .map(function(e) {
            return {
                name: e.name.replace(/[?].*$/, '').split('/').slice(-3).join('/'),
                start: Math.round(e.startTime),
                duration: Math.round(e.duration),
                size: e.transferSize
            };
        });
    return JSON.stringify({ops: ops, apis: resources});
})()
"""


class PerformanceMonitor:
    """Wraps a Selenium driver with performance instrumentation."""

    def __init__(self, driver):
        self.driver = driver
        self._active = False
        self._start_time = None
        self._results = {}

    def start(self, clear_buffer: bool = True):
        """Inject monitoring hooks.

        Args:
            clear_buffer: If True, clear resource timing buffer (for
                         interaction-only measurement). If False, keep
                         existing entries (for page load measurement).
        """
        self.driver.execute_script(_HOOK_JS)
        clear_js = (
            "performance.clearResourceTimings(); " "performance.setResourceTimingBufferSize(5000); "
            if clear_buffer
            else "performance.setResourceTimingBufferSize(5000); "
        )
        self.driver.execute_script(clear_js + "window.__perf_ops = [];")
        self._active = True
        self._start_time = time.time()

    def collect_page_load(self) -> list:
        """Collect API timings from page load (call after page loads).

        Does NOT require start() first — reads the existing resource
        timing buffer directly. Use this for measuring page load APIs.
        """
        try:
            raw = self.driver.execute_script("""
                var resources = performance.getEntriesByType('resource')
                    .filter(function(e) {
                        return e.initiatorType === 'xmlhttprequest'
                            || e.initiatorType === 'fetch';
                    })
                    .map(function(e) {
                        return {
                            name: e.name.split('?')[0].split('/').slice(-3).join('/'),
                            start: Math.round(e.startTime),
                            duration: Math.round(e.duration),
                            size: e.transferSize
                        };
                    });
                return JSON.stringify(resources);
                """)
            if not raw:
                return []
            return json.loads(raw)
        except Exception as e:
            print(f"  [perf_debug] collect_page_load error: {e}")
            return []

    def stop(self):
        """Collect timing data from the browser."""
        if not self._active:
            return {}
        raw = self.driver.execute_script(f"return {_DUMP_JS}")
        self._results = json.loads(raw) if raw else {"ops": [], "apis": []}
        self._results["wall_time"] = round(time.time() - self._start_time, 2)
        self._active = False
        return self._results

    def get_api_timings(self):
        """Return list of API call timings (name, start, duration, size)."""
        if self._active:
            self.stop()
        return self._results.get("apis", [])

    def get_click_log(self):
        """Return list of click/input events with timestamps."""
        if self._active:
            self.stop()
        return self._results.get("ops", [])

    def get_slow_apis(self, threshold_ms=3000):
        """Return APIs slower than threshold (default 3s)."""
        return [a for a in self.get_api_timings() if a["duration"] > threshold_ms]

    def mark(self, tag):
        """Insert a named marker at the current time."""
        import json as _json

        self.driver.execute_script(
            "var m = " + _json.dumps({"t": "performance.now()", "type": "mark", "tag": tag}) + ";"
            "m.t = performance.now(); window.__perf_ops.push(m);"
        )

    def attach_to_allure(self, test_name="perf"):
        """Attach performance data to Allure report as JSON + summary."""
        import allure

        data = self.stop()

        # Full data as JSON attachment
        allure.attach(
            json.dumps(data, indent=2, ensure_ascii=False),
            name=f"{test_name}_perf_data",
            attachment_type=allure.attachment_type.JSON,
        )

        # Human-readable summary
        apis = data.get("apis", [])
        if apis:
            slow = self.get_slow_apis()
            summary_lines = [
                f"Test: {test_name}",
                f"Wall time: {data.get('wall_time', 'N/A')}s",
                f"Total API calls: {len(apis)}",
                f"Slow APIs (>3s): {len(slow)}",
                "",
                "Top 10 slowest APIs:",
            ]
            sorted_apis = sorted(apis, key=lambda x: x["duration"], reverse=True)
            for a in sorted_apis[:10]:
                summary_lines.append(f"  {a['duration']}ms  {a['name']}")

            allure.attach(
                "\n".join(summary_lines),
                name=f"{test_name}_perf_summary",
                attachment_type=allure.attachment_type.TEXT,
            )

        return data

    def check_thresholds(self, thresholds=None):
        """Check API timings against thresholds. Returns list of violations.

        Args:
            thresholds: dict of {api_name_pattern: max_duration_ms}
        """
        if thresholds is None:
            thresholds = {}

        violations = []
        for api in self.get_api_timings():
            for pattern, limit in thresholds.items():
                if pattern in api["name"] and api["duration"] > limit:
                    violations.append(
                        {
                            "api": api["name"],
                            "duration_ms": api["duration"],
                            "threshold_ms": limit,
                            "exceeded_by_ms": api["duration"] - limit,
                        }
                    )
        return violations


class measure:
    """Context manager for measuring a specific operation."""

    def __init__(self, monitor, label):
        self.monitor = monitor
        self.label = label

    def __enter__(self):
        self.monitor.mark(f"{self.label}_start")
        return self

    def __exit__(self, *args):
        self.monitor.mark(f"{self.label}_end")
