"""效能報告管線單元測試（純資料，不需瀏覽器與環境）。

覆蓋 perf_reporting 的單一渲染路徑：KPI 計算、Allure 附件 HTML 的
關鍵區塊、門檻違規呈現與歷史趨勢記錄。CI regression 可直接跑。
"""

import json

import pytest

from tools.perf_reporting import (
    build_report_html,
    compute_kpis,
    record_history,
)


def _sample_apis():
    return [
        {
            "name": f"api/checkout/save_{i}",
            "start": i * 100,
            "duration": 500 + i * 900,
            "size": 100 + i,
        }
        for i in range(6)
    ]


@pytest.fixture
def history_file(tmp_path, monkeypatch):
    """把歷史檔導到 tmp，不污染工作目錄"""
    import tools.perf_reporting as pr

    monkeypatch.setattr(pr, "HISTORY_PATH", tmp_path / "history.json")
    yield pr.HISTORY_PATH


class TestKpis:
    def test_compute_kpis_basic(self):
        kpis = compute_kpis([{"duration": 100}, {"duration": 300}, {"duration": 4000}])
        assert kpis["api_count"] == 3
        assert kpis["slow_over_3s"] == 1
        assert kpis["max_ms"] == 4000

    def test_compute_kpis_empty(self):
        kpis = compute_kpis([])
        assert kpis["api_count"] == 0
        assert kpis["p95_ms"] is None


class TestReportHtml:
    def test_standalone_has_shell_and_sections(self):
        apis = _sample_apis()
        html = build_report_html(
            apis,
            {"test": "單元測試", "env": "QA", "date": "2026-11-09"},
            wall_time=12.3,
            standalone=True,
        )
        assert html.startswith("<!DOCTYPE html>")
        # KPI、量級條、全部明細表格都應存在
        assert "API p95" in html
        assert "pr-bar" in html
        assert "全部 API 明細" in html
        assert "單元測試" in html

    def test_attachment_fragment_has_no_page_shell(self):
        html = build_report_html(_sample_apis(), {"test": "x"})
        assert not html.startswith("<!DOCTYPE")
        assert "pr-wrap" in html

    def test_thresholds_pass_and_fail_chips(self):
        apis = [{"name": "booking/save", "start": 0, "duration": 2000}]
        ok = build_report_html(apis, {}, thresholds={"booking": 3000})
        assert "✓ PASS" in ok and "✓ 全數通過" in ok
        bad = build_report_html(apis, {}, thresholds={"booking": 1000})
        assert "✕ FAIL" in bad and "門檻違規" in bad and "+1.00s" in bad

    def test_names_are_escaped(self):
        apis = [{"name": "<script>alert(1)</script>", "start": 0, "duration": 10}]
        html = build_report_html(apis, {})
        assert "<script>alert" not in html
        assert "&lt;script&gt;" in html


class TestHistory:
    def test_record_and_trend(self, history_file):
        for _ in range(3):
            record_history(
                "unit_test",
                {"api_count": 10, "p95_ms": 900, "max_ms": 2000, "slow_over_3s": 0},
                {"env": "QA"},
            )
        data = json.loads(history_file.read_text(encoding="utf-8"))
        assert len(data["unit_test"]) == 3
        html = build_report_html(_sample_apis(), {}, test_name="unit_test", thresholds=None)
        assert "歷史趨勢" in html

    def test_history_keeps_last_n(self, history_file):
        for i in range(25):
            record_history("unit_test", {"api_count": i}, {})
        data = json.loads(history_file.read_text(encoding="utf-8"))
        assert len(data["unit_test"]) == 20
