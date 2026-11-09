"""效能報告統合模組：單一渲染路徑，同時供 Allure 附件與獨立 HTML 匯出。

設計原則：
- 視覺對齊 Allure2 預設主題（同字體、卡片、邊框與留白），附件在
  Allure 內開啟時風格一致；獨立檔案外殼僅多一層頁面背景。
- 量級（API 耗時）用單一色相明度漸層；狀態（PASS/FAIL、趨勢好壞）
  用保留色且必帶圖示＋文字，不單獨以顏色表達。
- 一切數字皆有表格檢視（可及性）。
- 歷史趨勢：perf-reports/history.json 每輪累積，報告內顯示與前輪
  的差異晶片與近 N 輪對照表。
"""

import html
import json
import os
from datetime import datetime
from pathlib import Path

HISTORY_PATH = Path("perf-reports") / "history.json"
HISTORY_KEEP_PER_TEST = 20

# Allure2 對齊的視覺 token（light）
_TOKENS = """
<style>
  .pr-wrap { font-family: Inter, 'Segoe UI', system-ui, sans-serif; color: #0b0b0b;
             font-size: 13px; line-height: 1.45; }
  .pr-wrap * { box-sizing: border-box; }
  .pr-card { background: #ffffff; border: 1px solid #e8e8e8; border-radius: 4px;
             padding: 14px 16px; margin: 12px 0; }
  .pr-h1 { font-size: 17px; font-weight: 700; margin: 0; }
  .pr-sub { color: #6a6a6a; font-size: 12px; margin-top: 2px; }
  .pr-h2 { font-size: 13px; font-weight: 700; margin: 0 0 10px; }
  .pr-tiles { display: flex; gap: 10px; flex-wrap: wrap; }
  .pr-tile { flex: 1 1 130px; border: 1px solid #e8e8e8; border-radius: 4px;
             padding: 10px 12px; background: #fafafa; }
  .pr-tile .pr-k { font-size: 11px; color: #6a6a6a; }
  .pr-tile .pr-v { font-size: 20px; font-weight: 700; margin-top: 2px; }
  .pr-delta { font-size: 11px; font-weight: 600; margin-top: 2px; }
  .pr-up { color: #d03b3b; }      /* 變慢＝bad */
  .pr-down { color: #1f8f4d; }    /* 變快＝good */
  .pr-flat { color: #6a6a6a; }
  .pr-chip { display: inline-block; font-size: 11px; font-weight: 700;
             border-radius: 3px; padding: 2px 8px; vertical-align: middle; }
  .pr-chip.pass { color: #1f8f4d; background: rgba(31,143,77,.12); }
  .pr-chip.fail { color: #d03b3b; background: rgba(208,59,59,.12); }
  .pr-chip.warn { color: #c76a00; background: rgba(199,106,0,.12); }
  table { border-collapse: collapse; width: 100%; font-size: 12px; }
  th, td { padding: 5px 8px; text-align: left; border-bottom: 1px solid #eeeeee; }
  th { color: #6a6a6a; font-weight: 600; font-size: 11px; text-transform: none; }
  tr:last-child td { border-bottom: none; }
  .pr-bar-row { display: flex; align-items: center; gap: 8px; margin: 3px 0; }
  .pr-bar-name { flex: 0 0 42%; overflow-wrap: anywhere; color: #0b0b0b; }
  .pr-root { font-size: 11px; color: #6a6a6a; margin: 2px 0 6px; }
  .pr-root code { background: #f0f2f5; border-radius: 3px; padding: 1px 5px;
                  font-size: 11px; color: #1758bf; }
  .pr-sub-inline { color: #999; margin-left: 4px; }
  td.api-name { overflow-wrap: anywhere; }
  .pr-bar-track { flex: 1 1 auto; }
  .pr-bar { height: 10px; border-radius: 4px 2px 2px 4px; background: #1758bf; }
  .pr-bar-val { flex: 0 0 auto; color: #0b0b0b; font-variant-numeric: tabular-nums; }
  details { margin-top: 6px; }
  summary { cursor: pointer; color: #1758bf; font-size: 12px; }
</style>
"""


def _esc(text) -> str:
    return html.escape(str(text))


def format_ms(ms):
    """毫秒 → 人類可讀（與 perf_analyzer.format_duration 同規則，避免循環依賴）"""
    if ms is None:
        return "N/A"
    if ms < 1000:
        return f"{ms:.0f}ms"
    return f"{ms / 1000:.2f}s"


def _pct(delta, base):
    if base in (None, 0):
        return None
    return (delta - base) / base * 100


def _delta_chip(now, prev, lower_is_better=True):
    """與前輪比較的差異晶片：必帶方向圖示＋數字（不單獨依賴顏色）"""
    if prev is None or now is None:
        return ""
    p = _pct(now - prev, prev)
    if p is None or abs(p) < 1:
        return f"<div class='pr-delta pr-flat'>— 無明顯變化</div>"
    arrow, cls = ("▲", "pr-up") if p > 0 else ("▼", "pr-down")
    if not lower_is_better:
        cls = "pr-down" if p > 0 else "pr-up"
    sign = "+" if p > 0 else ""
    return f"<div class='pr-delta {cls}'>{arrow} {sign}{p:.0f}% vs 前輪</div>"


def _tile(label, value, now=None, prev=None, lower_is_better=True):
    return (
        f"<div class='pr-tile'><div class='pr-k'>{_esc(label)}</div>"
        f"<div class='pr-v'>{_esc(value)}</div>"
        f"{_delta_chip(now, prev, lower_is_better)}</div>"
    )


def _common_root(names):
    """取共用的路徑前綴（以 / 分段比對）。少於 2 筆或無共用段則回傳 None。"""
    path_names = [n for n in names if "/" in n]
    if len(path_names) < 2:
        return None
    segments = [n.split("/") for n in path_names]
    common = []
    for seg in zip(*segments):
        if all(s == seg[0] for s in seg):
            common.append(seg[0])
        else:
            break
    # 至少要有一個以��的共用段，且不能等於完整名稱（全同名無意義）
    if len(common) < 1 or all(len(s) == len(common) for s in segments):
        return None
    root = "/".join(common) + "/"
    # 混合不同主機時只會剩下 scheme（https://）——無資訊量，不標註
    if root.rstrip("/") in ("https:", "http:"):
        return None
    return root


def _bar_rows(apis, top=12):
    """量級條：單一色相、明度隨值漸深（透明度衰減＝同色相漸層）。

    各列只顯示扣除共同根路徑後的差異段（游標停留顯示全名），
    欄位允許換行、不刪節。
    """
    root = _common_root([a["name"] for a in apis])
    rows = []
    if root:
        rows.append(
            f"<div class='pr-root'>共同根路徑 <code>{_esc(root)}</code>"
            f"<span class='pr-sub-inline'>（各列顯示其後差異段）</span></div>"
        )
    max_v = apis[0]["duration"] if apis else 1
    for a in apis[:top]:
        ratio = a["duration"] / max_v if max_v else 0
        alpha = 0.35 + 0.65 * ratio  # 明度單調：值越大越深
        w = max(ratio * 100, 0.8)
        shown = a["name"][len(root) :] if root and a["name"].startswith(root) else a["name"]
        rows.append(
            f"<div class='pr-bar-row'>"
            f"<span class='pr-bar-name' title='{_esc(a['name'])}'>{_esc(shown)}</span>"
            f"<span class='pr-bar-track'><span class='pr-bar' "
            f"style='width:{w:.1f}%;opacity:{alpha:.2f}'></span></span>"
            f"<span class='pr-bar-val'>{format_ms(a['duration'])}</span></div>"
        )
    return "".join(rows)


def _table(headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{head}</tr>{body}</table>"


def compute_kpis(apis, wall_time=None):
    """從 API 清單算 KPI（p95/最大值/慢於3s數量）"""
    durations = sorted(a["duration"] for a in apis)
    n = len(durations)
    p95 = durations[max(0, int(n * 0.95) - 1)] if n else None
    return {
        "api_count": n,
        "p95_ms": p95,
        "max_ms": durations[-1] if n else None,
        "slow_over_3s": sum(1 for d in durations if d > 3000),
        "wall_time": wall_time,
    }


def load_history():
    if HISTORY_PATH.exists():
        try:
            return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def record_history(test_name: str, kpis: dict, meta: dict) -> dict | None:
    """記錄本輪 KPI，回傳「前一輪」紀錄（供差異比較）。失敗不影響測試。"""
    try:
        hist = load_history()
        entries = hist.setdefault(test_name, [])
        prev = entries[-1] if entries else None
        entries.append(
            {
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "env": meta.get("env", ""),
                **{k: v for k, v in kpis.items() if v is not None},
            }
        )
        hist[test_name] = entries[-HISTORY_KEEP_PER_TEST:]
        HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_PATH.write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")
        return prev
    except OSError as e:
        print(f"  [perf] history 記錄失敗（不影響測試）: {e}")
        return None


def _trend_section(test_name: str, hist: dict):
    entries = hist.get(test_name, [])
    if len(entries) < 2:
        return ""
    rows = []
    for e in entries[-8:][::-1]:
        rows.append(
            [
                _esc(e.get("ts", "")),
                _esc(e.get("env", "")),
                str(e.get("api_count", "")),
                format_ms(e.get("p95_ms")),
                format_ms(e.get("max_ms")),
                str(e.get("slow_over_3s", "")),
            ]
        )
    return (
        "<div class='pr-card'><h2 class='pr-h2'>歷史趨勢（近 8 輪）</h2>"
        + _table(["時間", "環境", "API 數", "p95", "最大", ">3s"], rows)
        + "</div>"
    )


def build_report_html(
    apis,
    metadata: dict,
    wall_time=None,
    thresholds: dict | None = None,
    test_name: str | None = None,
    standalone: bool = False,
    rounds: list | None = None,
    save_stats: dict | None = None,
    recalc_stats: dict | None = None,
) -> str:
    """產生效能報告 HTML（Allure 附件與獨立檔案共用此一路徑）。

    Args:
        apis: API 清單（name/start/duration/size）
        metadata: test/env/date 顯示資訊
        wall_time: 總耗時（秒）
        thresholds: {api_pattern: max_ms}；違規會列為 FAIL 區塊
        test_name: 歷史記錄鍵（None＝不查趨勢）
        standalone: True 時加頁面外殼（獨立檔案用）
        rounds/save_stats/recalc_stats: booking 流程的輪次與統計（選填）
    """
    kpis = compute_kpis(apis, wall_time)
    hist = load_history() if test_name else {}
    prev = hist.get(test_name, [{}])[-1] if test_name and hist.get(test_name) else None
    prev_kpis = (
        compute_kpis([], None)
        if not prev
        else {
            "api_count": prev.get("api_count"),
            "p95_ms": prev.get("p95_ms"),
            "max_ms": prev.get("max_ms"),
            "slow_over_3s": prev.get("slow_over_3s"),
            "wall_time": prev.get("wall_time"),
        }
    )

    violations = []
    for api in apis:
        for pattern, limit in (thresholds or {}).items():
            if pattern in api.get("name", "") and api["duration"] > limit:
                violations.append(
                    {
                        "api": api["name"],
                        "duration_ms": api["duration"],
                        "threshold_ms": limit,
                        "exceeded_by_ms": api["duration"] - limit,
                    }
                )

    meta = metadata or {}
    chip = ""
    if thresholds is not None:
        chip = (
            f"<span class='pr-chip fail'>✕ FAIL</span>"
            if violations
            else "<span class='pr-chip pass'>✓ PASS</span>"
        )

    tiles = [
        _tile("API 總數", str(kpis["api_count"]), kpis["api_count"], prev_kpis["api_count"]),
        _tile("API p95", format_ms(kpis["p95_ms"]), kpis["p95_ms"], prev_kpis["p95_ms"]),
        _tile("最慢 API", format_ms(kpis["max_ms"]), kpis["max_ms"], prev_kpis["max_ms"]),
        _tile(
            ">3s 慢速 API",
            str(kpis["slow_over_3s"]),
            kpis["slow_over_3s"],
            prev_kpis["slow_over_3s"],
        ),
    ]
    if wall_time is not None:
        tiles.append(_tile("總耗時", f"{wall_time:.1f}s", wall_time, prev_kpis["wall_time"]))
    if save_stats and save_stats.get("count"):
        tiles.append(
            _tile(
                "Save 中位數", format_ms(save_stats.get("median")), save_stats.get("median"), None
            )
        )
    if recalc_stats and recalc_stats.get("count"):
        tiles.append(
            _tile(
                "Recalc 中位數",
                format_ms(recalc_stats.get("median")),
                recalc_stats.get("median"),
                None,
            )
        )

    parts = [f"<div class='pr-wrap'>"]
    parts.append(
        f"<div class='pr-card'><div class='pr-h1'>{_esc(meta.get('test', 'Performance Report'))}"
        f" {chip}</div>"
        f"<div class='pr-sub'>環境 {_esc(meta.get('env', 'N/A'))} · "
        f"{_esc(meta.get('date', datetime.now().strftime('%Y-%m-%d %H:%M')))}</div></div>"
    )
    parts.append(f"<div class='pr-tiles'>{''.join(tiles)}</div>")

    slowest = sorted(apis, key=lambda x: x["duration"], reverse=True)
    if slowest:
        parts.append(
            "<div class='pr-card'><h2 class='pr-h2'>最慢 API（Top 12）</h2>"
            + _bar_rows(slowest)
            + "</div>"
        )

    if rounds:
        rows = [
            [
                str(i),
                format_ms(r.get("save_duration_ms")),
                format_ms(r.get("recalc_duration_ms")),
                str(len(r.get("apis", []))),
            ]
            for i, r in enumerate(rounds, 1)
        ]
        parts.append(
            "<div class='pr-card'><h2 class='pr-h2'>輪次明細</h2>"
            + _table(["輪次", "Save API", "Recalculate", "API 數"], rows)
            + "</div>"
        )

    if violations:
        rows = [
            [
                _esc(v["api"]),
                format_ms(v["duration_ms"]),
                format_ms(v["threshold_ms"]),
                f"<span class='pr-chip fail'>▲ +{format_ms(v['exceeded_by_ms'])}</span>",
            ]
            for v in violations
        ]
        parts.append(
            "<div class='pr-card'><h2 class='pr-h2'>門檻違規（"
            f"{len(violations)} 筆）</h2>"
            + _table(["API", "耗時", "門檻", "超出"], rows)
            + "</div>"
        )
    elif thresholds is not None:
        parts.append(
            "<div class='pr-card'><h2 class='pr-h2'>門檻檢查</h2>"
            "<span class='pr-chip pass'>✓ 全數通過</span></div>"
        )

    if test_name:
        trend = _trend_section(test_name, hist)
        if trend:
            parts.append(trend)

    if slowest:
        table_root = _common_root([a["name"] for a in slowest])
        root_line = (
            f"<div class='pr-root'>共同根路徑 <code>{_esc(table_root)}</code>"
            f"<span class='pr-sub-inline'>（下表 API 欄顯示其後差異段）</span></div>"
            if table_root
            else ""
        )
        rows = [
            [
                str(i),
                _esc(
                    a["name"][len(table_root) :]
                    if table_root and a["name"].startswith(table_root)
                    else a["name"]
                ),
                format_ms(a["duration"]),
                str(a.get("size", "")),
            ]
            for i, a in enumerate(slowest, 1)
        ]
        parts.append(
            "<div class='pr-card'><details open><summary>全部 API 明細</summary>"
            + root_line
            + _table(["#", "API", "耗時", "Size"], rows)
            + "</details></div>"
        )
    parts.append("</div>")

    body = _TOKENS + "".join(parts)
    if standalone:
        return (
            "<!DOCTYPE html><html><head><meta charset='UTF-8'>"
            "<title>Performance Report</title>"
            "<style>body{background:#f6f6f6;margin:0;padding:20px}</style>"
            "</head><body>" + body + "</body></html>"
        )
    return body


def emit(
    apis,
    metadata: dict,
    test_name: str,
    wall_time=None,
    thresholds: dict | None = None,
    rounds: list | None = None,
    save_stats: dict | None = None,
    recalc_stats: dict | None = None,
):
    """統合輸出：Allure 附件（HTML+JSON）＋ 歷史記錄 ＋ 獨立檔案匯出。

    回傳 (kpis, prev) 供測試端斷言使用。
    """
    import allure

    kpis = compute_kpis(apis, wall_time)
    prev = record_history(test_name, kpis, metadata or {})

    html_body = build_report_html(
        apis,
        metadata,
        wall_time=wall_time,
        thresholds=thresholds,
        test_name=test_name,
        rounds=rounds,
        save_stats=save_stats,
        recalc_stats=recalc_stats,
    )
    allure.attach(
        html_body, name=f"{test_name}_report", attachment_type=allure.attachment_type.HTML
    )
    allure.attach(
        json.dumps(
            {"kpis": kpis, "apis": apis, "rounds": rounds},
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        name=f"{test_name}_data",
        attachment_type=allure.attachment_type.JSON,
    )

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out = Path("perf-reports") / f"{test_name}_{ts}.html"
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            build_report_html(
                apis,
                metadata,
                wall_time=wall_time,
                thresholds=thresholds,
                test_name=test_name,
                standalone=True,
                rounds=rounds,
                save_stats=save_stats,
                recalc_stats=recalc_stats,
            ),
            encoding="utf-8",
        )
        print(f"  [perf] report: {out}")
    except OSError as e:
        print(f"  [perf] 獨立報告寫檔失敗（不影響測試）: {e}")
    return kpis, prev


def write_environment_properties(config):
    """把執行環境寫進 allure-results/environment.properties（Allure 環境面板）。"""
    alluredir = config.getoption("--alluredir", None) if config else None
    if not alluredir:
        return
    props = {
        "ENV": os.getenv("ENV", ""),
        "ENV_NUM": os.getenv("ENV_NUM", ""),
        "VERSION": os.getenv("VERSION", ""),
        "WEB_URL": os.getenv("WEB_URL", ""),
        "Browser": "Chrome (local)" if not os.getenv("SELENIUM_HUB") else os.getenv("SELENIUM_HUB"),
    }
    try:
        Path(alluredir).mkdir(parents=True, exist_ok=True)
        content = "\n".join(f"{k}={v}" for k, v in props.items() if v) + "\n"
        (Path(alluredir) / "environment.properties").write_text(content, encoding="utf-8")
    except OSError as e:
        print(f"  [perf] environment.properties 寫入失敗: {e}")
