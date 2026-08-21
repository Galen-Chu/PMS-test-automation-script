"""
Selenium CLI - Browser automation CLI for Athena PMS locator discovery.
Session persists between invocations via session_storages.json.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
    StaleElementReferenceException,
)

SESSION_FILE = Path(__file__).parent / "session.json"
BROWSER_SESSION_FILE = Path(__file__).parent / "session.json"
PROJECT_SESSION_FILE = Path(__file__).parent / "session_storages.json"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"
DIFF_SNAPSHOT_FILE = Path(__file__).parent / ".diff_snapshot.json"
LAST_OP_FILE = Path(__file__).parent / ".last_op.json"
POM_OUTPUT_FILE = Path(__file__).parent / "pom_output.py"

SPECIAL_KEYS = {
    "enter": Keys.ENTER,
    "return": Keys.RETURN,
    "tab": Keys.TAB,
    "escape": Keys.ESCAPE,
    "esc": Keys.ESCAPE,
    "backspace": Keys.BACKSPACE,
    "delete": Keys.DELETE,
    "up": Keys.ARROW_UP,
    "down": Keys.ARROW_DOWN,
    "left": Keys.ARROW_LEFT,
    "right": Keys.ARROW_RIGHT,
    "home": Keys.HOME,
    "end": Keys.END,
    "pageup": Keys.PAGE_UP,
    "pagedown": Keys.PAGE_DOWN,
    "f5": Keys.F5,
}


def _read_pytest_ini(key):
    ini_path = Path(__file__).resolve().parent.parent / "pytest.ini"
    if not ini_path.exists():
        return None
    with open(ini_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == key and v.strip():
                return v.strip()
    return None


# ─── Session Management ─────────────────────────────────────────


def _save_session(hub_url, session_id):
    existing = {}
    if SESSION_FILE.exists():
        try:
            existing = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            pass
    existing["hub_url"] = hub_url
    existing["session_id"] = session_id
    SESSION_FILE.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


def _load_session():
    if not SESSION_FILE.exists():
        print("ERROR: No active session. Run 'connect' first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(SESSION_FILE.read_text(encoding="utf-8"))


def _get_driver():
    session = _load_session()
    original = RemoteWebDriver.execute

    def patched(self, command, params=None):
        if command == "newSession":
            return {"value": {"sessionId": session["session_id"], "capabilities": {}}}
        return original(self, command, params)

    RemoteWebDriver.execute = patched
    try:
        driver = webdriver.Remote(command_executor=session["hub_url"], options=ChromeOptions())
        driver.session_id = session["session_id"]
    finally:
        RemoteWebDriver.execute = original

    driver.implicitly_wait(5)
    return driver


# ─── Last Operation Tracking ────────────────────────────────────


def _save_last_op(op_type, by, selector):
    by_name = "XPATH" if by == By.XPATH else "CSS_SELECTOR"
    data = {"op_type": op_type, "by": by_name, "selector": selector}
    LAST_OP_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ─── Helpers ─────────────────────────────────────────────────────


def _resolve_locator(args):
    if getattr(args, "css", None):
        return By.CSS_SELECTOR, args.css
    if getattr(args, "xpath_file", None):
        with open(args.xpath_file, encoding="utf-8") as f:
            return By.XPATH, f.read().strip()
    return By.XPATH, args.xpath


def _suggest_xpath(tag, attrs):
    dfid = attrs.get("data-field-id")
    if dfid:
        return f"//{tag}[@data-field-id='{dfid}']"

    parent_dfid = attrs.get("_parent_dfid")
    if parent_dfid:
        return f"//div[@data-field-id='{parent_dfid}']//{tag}"

    field = attrs.get("field")
    if field and tag == "td":
        return f"//td[@field='{field}']"

    elem_id = attrs.get("id")
    if elem_id and not elem_id.startswith("el-") and len(elem_id) < 50:
        return f"//{tag}[@id='{elem_id}']"

    name = attrs.get("name")
    if name:
        return f"//{tag}[@name='{name}']"

    text = attrs.get("_text", "").strip()
    if text and tag in ("button", "a") and len(text) < 30:
        return f"//{tag}[normalize-space()='{text}']"

    title = attrs.get("title")
    if title and len(title) < 40:
        return f"//{tag}[@title='{title}']"

    cls = attrs.get("class")
    if cls and tag not in ("input", "textarea", "select", "button"):
        classes = [
            c for c in cls.split() if c and not c.startswith("e-") and not c.startswith("el-")
        ]
        if classes:
            return f"//{tag}[contains(@class,'{classes[0]}')]"

    return None


SCAN_ATTRS = [
    "id",
    "name",
    "data-field-id",
    "type",
    "class",
    "value",
    "placeholder",
    "title",
    "aria-label",
    "field",
    "readonly",
    "disabled",
    "role",
    "data-vv-as",
]

KEY_ATTRS = ["data-field-id", "field", "name", "id", "type", "placeholder"]

_SCAN_JS = r"""
const ALL_ATTRS = ["id", "name", "data-field-id", "type", "class", "value",
    "placeholder", "title", "aria-label", "field", "readonly",
    "disabled", "role", "data-vv-as"];
const KEY_ATTRS = ["data-field-id", "field", "name", "id", "type", "placeholder"];

const interactiveRoles = ["button", "link", "tab", "option", "menuitem",
    "treeitem", "gridcell", "checkbox", "radio", "switch", "combobox",
    "searchbox", "textbox"];

function getAttrs(el) {
    const attrs = {};
    for (const k of ALL_ATTRS) {
        const v = el.getAttribute(k);
        if (v && v !== "null" && v !== "undefined") {
            attrs[k] = k === "class" ? v.substring(0, 80) : v;
        }
    }
    const text = (el.textContent || "").trim().substring(0, 60);
    if (text) attrs._text = text;
    const img = el.querySelector("img[alt]");
    if (img) attrs._img_alt = img.getAttribute("alt");
    return attrs;
}

function suggestXpath(tag, attrs) {
    const dfid = attrs["data-field-id"];
    if (dfid) return "//" + tag + "[@data-field-id='" + dfid + "']";
    const parentDfid = attrs._parent_dfid;
    if (parentDfid) return "//div[@data-field-id='" + parentDfid + "']//" + tag;
    const field = attrs.field;
    if (field && tag === "td") return "//td[@field='" + field + "']";
    const elemId = attrs.id;
    if (elemId && !elemId.startsWith("el-") && elemId.length < 50)
        return "//" + tag + "[@id='" + elemId + "']";
    const name = attrs.name;
    if (name) return "//" + tag + "[@name='" + name + "']";
    const text = (attrs._text || "").trim();
    if (text && (tag === "button" || tag === "a") && text.length < 30) {
        if (/\d/.test(text)) {
            const prefix = text.replace(/[\d,]+\s*$/, "").trim();
            if (prefix) return "//" + tag + "[starts-with(normalize-space(),'" + prefix + "')]";
            return "//" + tag + "[contains(normalize-space(),'" + text.replace(/[\d,\s]+/g, "").trim() + "')]";
        }
        return "//" + tag + "[normalize-space()='" + text + "']";
    }
    const title = attrs.title;
    if (title && title.length < 40) return "//" + tag + "[@title='" + title + "']";
    const cls = attrs["class"];
    if (cls && !["input", "textarea", "select", "button"].includes(tag)) {
        const classes = cls.split(/\\s+/).filter(c => c && !c.startsWith("e-") && !c.startsWith("el-"));
        if (classes.length) return "//" + tag + "[contains(@class,'" + classes[0] + "')]";
    }
    return null;
}

function getContext(el) {
    let parentDfid = null, labelText = null, tdDfid = null;
    try {
        const ancestor = el.closest("[data-field-id]");
        if (ancestor) parentDfid = ancestor.getAttribute("data-field-id");
        const tdAncestor = el.closest("td[data-field-id]");
        if (tdAncestor && tdAncestor !== el) tdDfid = tdAncestor.getAttribute("data-field-id");
        const tag = el.tagName;
        if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") {
            const parent = el.closest("div");
            if (parent) {
                const prev = parent.previousElementSibling;
                if (prev && prev.tagName === "LABEL") {
                    labelText = (prev.getAttribute("title") || prev.textContent.trim()).substring(0, 60);
                }
                if (!labelText) {
                    const labels = parent.querySelectorAll("label[title]");
                    if (labels.length) labelText = labels[0].getAttribute("title");
                }
            }
        }
    } catch(e) {}
    return { parentDfid, labelText, tdDfid };
}

const scopeSelector = arguments[0] || null;
const includeHidden = arguments[1] || false;
const includeAll = arguments[2] || false;

let root = document;
if (scopeSelector) {
    const scopeEl = document.querySelector(scopeSelector);
    if (scopeEl) root = scopeEl;
}

const tagGroups = [
    ["Inputs", "input"], ["Textareas", "textarea"],
    ["Selects", "select"], ["Buttons", "button"]
];
if (includeAll) {
    tagGroups.push(["Links", "a"], ["Labels", "label"]);
}

const results = { groups: {}, roles: [], gridColumns: [], frameworks: {} };

const scope = scopeSelector ? (document.querySelector(scopeSelector) || document) : document;
results.frameworks = {
    syncfusion: scope.querySelectorAll("[data-field-id], [class*='e-control'], .e-grid, .e-dialog").length,
    easyui: scope.querySelectorAll(".panel-title, .datagrid, .combobox-item, [datagrid-row-index]").length,
    elementui: scope.querySelectorAll(".el-select, .el-dialog, .el-date-table, .el-message-box").length
};

for (const [groupName, tag] of tagGroups) {
    const elements = root.getElementsByTagName(tag);
    const items = [];
    for (const el of elements) {
        if (!includeHidden && !el.offsetWidth && !el.offsetHeight) continue;
        const attrs = getAttrs(el);
        const ctx = getContext(el);
        if (!attrs["data-field-id"] && ctx.parentDfid) attrs._parent_dfid = ctx.parentDfid;
        const xpath = suggestXpath(tag, attrs);
        const keyParts = KEY_ATTRS.filter(k => attrs[k]).map(k => k + '="' + attrs[k] + '"');
        items.push({
            tag, attrs, enabled: !el.disabled,
            labelText: ctx.labelText, parentDfid: ctx.parentDfid,
            xpath, keyParts
        });
    }
    if (items.length) results.groups[groupName] = items;
}

const allEls = root.getElementsByTagName("*");
const roleItems = [];
for (const el of allEls) {
    const role = el.getAttribute("role");
    if (!role || !interactiveRoles.includes(role)) continue;
    if (!includeHidden && !el.offsetWidth && !el.offsetHeight) continue;
    const tag = el.tagName.toLowerCase();
    if (["input", "textarea", "select", "button", "a"].includes(tag)) continue;
    const attrs = getAttrs(el);
    const ctx = getContext(el);
    if (!attrs["data-field-id"] && ctx.parentDfid) attrs._parent_dfid = ctx.parentDfid;
    const xpath = suggestXpath(tag, attrs);
    const keyParts = KEY_ATTRS.filter(k => attrs[k]).map(k => k + '="' + attrs[k] + '"');
    roleItems.push({
        tag, attrs, enabled: !el.disabled,
        labelText: ctx.labelText, parentDfid: ctx.parentDfid,
        xpath, keyParts
    });
}
if (roleItems.length) results.roles = roleItems;

const clickSelectors = [
    "a[class*='close'], a[class*='tool'], a[class*='panel-tool']",
    "i[class*='icon'], i[class*='fa-'], i[class*='glyphicon']",
    "span[class*='button'], span[class*='sub-button'], span[role='button'], span[onclick]",
    "label[data-field-id], label[onclick], label[role='button']"
];
const clickableItems = [];
for (const sel of clickSelectors) {
    const elements = root.querySelectorAll(sel);
    for (const el of elements) {
        const tag = el.tagName.toLowerCase();
        if (["input", "textarea", "select", "button"].includes(tag)) continue;
        if (interactiveRoles.includes(el.getAttribute("role"))) continue;
        if (!includeHidden && !el.offsetWidth && !el.offsetHeight) continue;
        const attrs = getAttrs(el);
        const ctx = getContext(el);
        if (!attrs["data-field-id"] && ctx.parentDfid) attrs._parent_dfid = ctx.parentDfid;
        if (ctx.tdDfid) attrs._td_dfid = ctx.tdDfid;
        const xpath = ctx.tdDfid
            ? "//td[@data-field-id='" + ctx.tdDfid + "']//" + tag
            : suggestXpath(tag, attrs);
        const keyParts = KEY_ATTRS.filter(k => attrs[k]).map(k => k + '="' + attrs[k] + '"');
        clickableItems.push({
            tag, attrs, enabled: !el.disabled,
            labelText: ctx.labelText, parentDfid: ctx.parentDfid,
            tdDfid: ctx.tdDfid, xpath, keyParts
        });
    }
}
if (clickableItems.length) results.clickable = clickableItems;

const includeVue = arguments[3] || false;
if (includeVue) {
    const standardTags = new Set(["input", "textarea", "select", "button", "a", "label"]);
    const interactivePatterns = /\\b(card|tab|menu|option|chip|badge|btn|action|toggle)\\b/i;
    const vueItems = [];
    const allEls2 = root.getElementsByTagName("*");
    const seen = new Map();
    for (const el of allEls2) {
        let hasDataV = false;
        for (const attr of el.attributes) {
            if (attr.name.startsWith("data-v-")) { hasDataV = true; break; }
        }
        if (!hasDataV) continue;
        const tag = el.tagName.toLowerCase();
        if (standardTags.has(tag)) continue;
        if (!includeHidden && !el.offsetWidth && !el.offsetHeight) continue;
        const style = window.getComputedStyle(el);
        const hasPointer = style.cursor === "pointer";
        const hasOnclick = el.hasAttribute("onclick");
        const cls = typeof el.className === "string" ? el.className : "";
        const hasPattern = interactivePatterns.test(cls);
        if (!hasPointer && !hasOnclick && !hasPattern) continue;
        const key = tag + "|" + cls.substring(0, 50);
        if (seen.has(key)) { seen.set(key, seen.get(key) + 1); continue; }
        seen.set(key, 1);
        const attrs = getAttrs(el);
        const ctx = getContext(el);
        if (!attrs["data-field-id"] && ctx.parentDfid) attrs._parent_dfid = ctx.parentDfid;
        const xpath = suggestXpath(tag, attrs);
        const keyParts = KEY_ATTRS.filter(k => attrs[k]).map(k => k + '="' + attrs[k] + '"');
        let innerTag = null;
        if (tag === "li" || tag === "div") {
            const inner = el.querySelector("a, button");
            if (inner) innerTag = inner.tagName.toLowerCase();
        }
        vueItems.push({
            tag, attrs, enabled: !el.disabled,
            labelText: ctx.labelText, parentDfid: ctx.parentDfid,
            xpath, keyParts, _dedup_key: key, innerTag
        });
    }
    for (const item of vueItems) {
        const count = seen.get(item._dedup_key) || 1;
        if (count > 1) item._similar_count = count;
    }
    if (vueItems.length) results.vueComponents = vueItems;
}

const fields = {};
scope.querySelectorAll("tbody td[field], .datagrid-body td[field]").forEach(td => {
    const f = td.getAttribute("field");
    if (fields[f]) return;
    fields[f] = {
        field: f,
        hasInput: !!td.querySelector("input"),
        hasBtn: !!td.querySelector("button, span[class*='button']"),
        sample: (td.textContent || "").trim().substring(0, 30)
    };
});
results.gridColumns = Object.values(fields);

var gridSummary = [];
var easyuiRows = scope.querySelectorAll('tr[datagrid-row-index]');
var easyuiUnique = new Set(); easyuiRows.forEach(function(r){ easyuiUnique.add(r.getAttribute('datagrid-row-index')); });
if (easyuiUnique.size) {
    gridSummary.push({framework: 'easyui', count: easyuiUnique.size, sampleXpath: "//tr[@datagrid-row-index='0']"});
}
var sfRows = scope.querySelectorAll('.e-gridcontent .e-row');
if (sfRows.length) {
    var firstUid = sfRows[0].getAttribute('data-uid') || '';
    gridSummary.push({framework: 'syncfusion', count: sfRows.length, sampleXpath: firstUid ? "//tr[@data-uid='" + firstUid + "']" : "//div[contains(@class,'e-gridcontent')]//tr[contains(@class,'e-row')][1]"});
}
if (gridSummary.length) results.gridRows = gridSummary;

var cards = scope.querySelectorAll('.card--room');
if (cards.length) {
    var firstCardId = cards[0].id || '';
    results.customCards = {
        type: 'card--room',
        count: cards.length,
        sampleXpath: firstCardId ? "//div[@id='" + firstCardId + "']" : "//div[contains(@class,'card--room')][1]"
    };
}

return results;
"""


def _print_scan_item(index, item):
    tag = item["tag"]
    attrs = item["attrs"]
    enabled = item["enabled"]
    label_text = item.get("labelText")
    parent_dfid = item.get("parentDfid")
    xpath = item.get("xpath")
    key_parts = item.get("keyParts", [])

    status = "enabled" if enabled else "DISABLED"
    attr_str = " ".join(key_parts) if key_parts else "(no key attrs)"
    text = attrs.get("_text", "")

    print(f"  #{index}  <{tag}> {attr_str}  [{status}]")
    if label_text:
        print(f"       label: {label_text}")
    td_dfid = item.get("tdDfid")
    if td_dfid:
        print(f'       td: data-field-id="{td_dfid}"')
    if parent_dfid:
        print(f'       parent: data-field-id="{parent_dfid}"')
    if text:
        print(f"       text: {text}")
    img_alt = attrs.get("_img_alt")
    if img_alt:
        print(f"       img_alt: {img_alt}")
    inner_tag = item.get("innerTag")
    if inner_tag:
        print(f"       inner: <{inner_tag}>")
    if xpath:
        print(f"       -> {xpath}")


# ─── Commands ────────────────────────────────────────────────────

EDGE_DRIVER_PATH = os.getenv("EDGE_DRIVER", r"C:\Download\edgedriver\msedgedriver.exe")
EDGE_DRIVER_PORT = 9515


def _start_edge_driver_server():
    import subprocess

    try:
        import requests

        requests.get(f"http://localhost:{EDGE_DRIVER_PORT}/status", timeout=2)
        return
    except Exception:
        pass
    subprocess.Popen(
        [EDGE_DRIVER_PATH, f"--port={EDGE_DRIVER_PORT}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=0x00000008,
    )
    time.sleep(2)


def cmd_connect(args):
    hub_url = args.hub or os.getenv("SELENIUM_HUB") or _read_pytest_ini("SELENIUM_HUB")

    if SESSION_FILE.exists():
        try:
            old = _load_session()
            old_driver = _get_driver()
            old_driver.title
            _save_session(old["hub_url"], old["session_id"])
            print(f"Reusing existing session: {old['session_id']}")
            return
        except Exception:
            try:
                SESSION_FILE.unlink()
            except Exception:
                pass

    if hub_url:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--guest")
        options.add_argument("--disable-features=Credentials")
        options.add_argument("--disable-popup-blocking")
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2,
            },
        )
        driver = webdriver.Remote(command_executor=hub_url, options=options)
    elif args.edge:
        from selenium.webdriver.edge.options import Options as EdgeOptions

        _start_edge_driver_server()
        hub_url = f"http://localhost:{EDGE_DRIVER_PORT}"
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Remote(command_executor=hub_url, options=options)
    else:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--guest")
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )
        from selenium.webdriver.chrome.service import Service

        driver = webdriver.Chrome(service=Service(), options=options)
        hub_url = driver.command_executor._url

    driver.implicitly_wait(5)
    _save_session(hub_url, driver.session_id)
    print(f"Session: {driver.session_id}")


def cmd_attach(args):
    debug_port = args.port
    addr = f"127.0.0.1:{debug_port}"

    if args.edge:
        from selenium.webdriver.edge.options import Options as EdgeOptions

        _start_edge_driver_server()
        hub_url = f"http://localhost:{EDGE_DRIVER_PORT}"
        options = EdgeOptions()
        options.add_experimental_option("debuggerAddress", addr)
        driver = webdriver.Remote(command_executor=hub_url, options=options)
    else:
        options = ChromeOptions()
        options.add_experimental_option("debuggerAddress", addr)
        from selenium.webdriver.chrome.service import Service

        driver = webdriver.Chrome(service=Service(), options=options)
        hub_url = driver.command_executor._url

    _save_session(hub_url, driver.session_id)
    print(f"Attached on port {debug_port}")
    print(f"Session: {driver.session_id}")
    print(f"Tabs: {len(driver.window_handles)}")
    current = driver.current_window_handle
    for i, h in enumerate(driver.window_handles):
        try:
            driver.switch_to.window(h)
            print(f"  [{i}] {driver.title[:50]}{' <- active' if h == current else ''}")
        except WebDriverException:
            print(f"  [{i}] (inaccessible)")
    driver.switch_to.window(current)


def cmd_close(_args):
    driver = _get_driver()
    driver.quit()
    SESSION_FILE.unlink(missing_ok=True)
    print("Session closed.")


def cmd_save_browser_session(_args):
    driver = _get_driver()
    cookies = driver.get_cookies()
    session_storage = driver.execute_script("""
        let data = {};
        for (let [key, value] of Object.entries(sessionStorage)) {
            data[key] = value;
        }
        return data;
    """)
    current_url = driver.current_url
    existing = {}
    if SESSION_FILE.exists():
        try:
            existing = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            pass
    existing.update({"cookies": cookies, "session_storage": session_storage, "url": current_url})
    SESSION_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(cookies)} cookies + {len(session_storage)} sessionStorage entries")
    print(f"From: {current_url}")


def _enter_pms(driver):
    """Navigate from EIP into PMS SPA. Assumes currently on EIP page."""
    driver.execute_script("""
        var btns = document.querySelectorAll('button');
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].textContent.trim() === '確定') { btns[i].click(); break; }
        }
    """)
    time.sleep(3)

    for attempt in range(5):
        clicked = False
        try:
            clicked = driver.execute_script("""
            var cards = document.querySelectorAll('.systemcardtest');
            for (var i = 0; i < cards.length; i++) {
                if (cards[i].textContent.indexOf('PMS') >= 0) { cards[i].click(); return true; }
            }
            var links = document.querySelectorAll('a');
            for (var i = 0; i < links.length; i++) {
                if (links[i].textContent.trim() === 'PMS' || links[i].textContent.indexOf('PMS 飯店前檯系統') >= 0) { links[i].click(); return true; }
            }
            return false;
        """)
        except WebDriverException:
            break
        if clicked:
            break
        time.sleep(1)

    if not clicked:
        print("WARNING: PMS system card not found", file=sys.stderr)
        return

    old_heading = driver.execute_script(
        "return document.querySelector('.breadcrumb, .page-header, h1, h2')"
        "?.textContent?.trim()?.substring(0, 80)"
    )
    _wait_for_page(driver, old_heading)
    time.sleep(1)

    current = driver.current_url
    if "locale=undefined" in current:
        locale = driver.execute_script("return sessionStorage.getItem('locale')") or "zh_TW"
        fixed = current.replace("locale=undefined", f"locale={locale}")
        fixed = fixed.replace("_rand=undefined", "_rand=restored")
        driver.get(fixed)
        time.sleep(3)

    print(f"Entered PMS: {driver.current_url}")


def cmd_restore_browser_session(args):
    driver = _get_driver()
    if not BROWSER_SESSION_FILE.exists():
        print("ERROR: No browser session file. Run 'save-session' first.", file=sys.stderr)
        sys.exit(1)

    data = json.loads(BROWSER_SESSION_FILE.read_text(encoding="utf-8"))
    target_url = data["url"]

    from urllib.parse import urlparse

    parsed = urlparse(target_url)
    domain_root = f"{parsed.scheme}://{parsed.netloc}"
    driver.get(domain_root)
    time.sleep(1)

    for cookie in data["cookies"]:
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass

    session_storage = data.get("session_storage", {})
    if session_storage:
        driver.execute_script(
            """
            const data = arguments[0];
            for (const [key, value] of Object.entries(data)) {
                sessionStorage.setItem(key, value);
            }
        """,
            session_storage,
        )

    web_url = _read_pytest_ini("WEB_URL")
    env_num = _read_pytest_ini("ENV_NUM")
    if web_url and env_num:
        pms_landing = f"{web_url}/pms/{env_num}/reservation/PMS0110010"
        driver.get(pms_landing)
    else:
        driver.get(target_url)
    time.sleep(3)
    print(
        f"Restored {len(data['cookies'])} cookies + {len(session_storage)} sessionStorage entries"
    )

    driver.implicitly_wait(0)
    relogin_alert = driver.find_elements(By.XPATH, "//*[contains(text(),'重新登入')]")
    driver.implicitly_wait(5)

    if relogin_alert:
        print("Session expired — auto re-login...", flush=True)
        ok_btns = driver.find_elements(
            By.XPATH, "//div[@class='el-message-box__btns']//button | //div[@role='dialog']//button"
        )
        if ok_btns:
            ok_btns[0].click()
            time.sleep(1)

        class _FakeArgs:
            username = None
            password = None
            base_url = None
            redirect_url = None
            client_id = "internal"
            language = "zh-TW"
            company = None

        cmd_login(_FakeArgs())

        driver.get(pms_landing if (web_url and env_num) else target_url)
        time.sleep(3)

    print(f"URL: {driver.current_url}")


def _wait_for_page(driver, old_heading, timeout=10):
    for _ in range(timeout * 2):
        time.sleep(0.5)
        new_heading = driver.execute_script(
            "return document.querySelector('.breadcrumb, .page-header, h1, h2')"
            "?.textContent?.trim()?.substring(0, 80)"
        )
        if new_heading and new_heading != old_heading:
            return True
    return False


def cmd_nav(args):
    driver = _get_driver()
    old_heading = driver.execute_script(
        "return document.querySelector('.breadcrumb, .page-header, h1, h2')"
        "?.textContent?.trim()?.substring(0, 80)"
    )
    driver.get(args.url)
    if not args.no_wait:
        _wait_for_page(driver, old_heading)
    print(f"{driver.title}")
    print(f"{driver.current_url}")


def cmd_back(_args):
    driver = _get_driver()
    driver.back()
    time.sleep(0.5)
    print(f"{driver.title}")
    print(f"{driver.current_url}")


def _do_click(driver, args, by, selector):
    """Core click logic, extracted for reuse with _with_diff."""
    elements = driver.find_elements(by, selector)

    if not elements:
        raise NoSuchElementException(f"No elements found: {selector}")

    if len(elements) == 1:
        el = elements[0]
    else:
        visible_index = driver.execute_script(
            """
            var elements = arguments[0];
            for (var i = 0; i < elements.length; i++) {
                var rect = elements[i].getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) return i;
            }
            return -1;
        """,
            elements,
        )

        if visible_index < 0:
            print(
                f"ERROR: {len(elements)} elements match '{selector}' but all are 0x0 (hidden)",
                file=sys.stderr,
            )
            sys.exit(1)

        el = elements[visible_index]
        if visible_index > 0:
            print(f"Skipped {visible_index} hidden element(s), clicking #{visible_index + 1}")

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", el)

    if getattr(args, "js", False):
        driver.execute_script("arguments[0].click()", el)
        _save_last_op("click", by, selector)
        print(f"Clicked (JS forced): {selector}")
        return

    last_err = None
    for attempt in range(3):
        try:
            el.click()
            _save_last_op("click", by, selector)
            print(f"Clicked: {selector}")
            return
        except WebDriverException as e:
            last_err = e
            if attempt < 2:
                time.sleep(0.5)

    err_msg = str(last_err).split("\n")[0] if str(last_err) else "unknown"
    print(f"BLOCKED: Native click failed on {selector}")
    print(f"  Reason: {err_msg}")
    _print_failure_diagnostics(driver, el)
    print(f"  Hint: Use 'click --js -x \"...\"' to force JS click")
    sys.exit(1)


def cmd_click(args):
    driver = _get_driver()
    by, selector = _resolve_locator(args)

    if getattr(args, "diff", False):
        wait = getattr(args, "wait", 0) or 0
        _with_diff(driver, lambda: _do_click(driver, args, by, selector), wait_seconds=wait)
    else:
        _do_click(driver, args, by, selector)


def cmd_type(args):
    driver = _get_driver()
    by, selector = _resolve_locator(args)
    el = driver.find_element(by, selector)

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", el)
    time.sleep(0.2)

    if not args.append:
        original_value = el.get_attribute("value") or ""
        try:
            el.click()
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(args.text)
        except WebDriverException:
            if original_value:
                driver.execute_script("arguments[0].value = arguments[1]", el, original_value)
            print(f"ERROR: Cannot type into element: {selector}", file=sys.stderr)
            _print_failure_diagnostics(driver, el)
            raise
    else:
        try:
            el.send_keys(args.text)
        except WebDriverException:
            print(f"ERROR: Cannot type into element (append): {selector}", file=sys.stderr)
            _print_failure_diagnostics(driver, el)
            raise

    if args.enter:
        el.send_keys(Keys.ENTER)
    _save_last_op("type", by, selector)
    print(f"Typed into: {selector}")


def cmd_key(args):
    driver = _get_driver()
    key_name = args.key.lower()
    key = SPECIAL_KEYS.get(key_name)
    if not key:
        print(
            f"ERROR: Unknown key '{args.key}'. Available: {', '.join(SPECIAL_KEYS)}",
            file=sys.stderr,
        )
        sys.exit(1)

    if getattr(args, "xpath", None) or getattr(args, "css", None):
        by, selector = _resolve_locator(args)
        driver.find_element(by, selector).send_keys(key)
    else:
        from selenium.webdriver.common.action_chains import ActionChains

        ActionChains(driver).send_keys(key).perform()
    print(f"Sent key: {args.key}")


def cmd_text(args):
    driver = _get_driver()
    by, selector = _resolve_locator(args)
    print(driver.find_element(by, selector).text)


def cmd_attr(args):
    driver = _get_driver()
    by, selector = _resolve_locator(args)
    val = driver.find_element(by, selector).get_attribute(args.name)
    print(val if val is not None else "(null)")


_FIND_JS = r"""
const ALL_ATTRS = ["id", "name", "data-field-id", "type", "class", "value",
    "placeholder", "title", "aria-label", "field", "readonly",
    "disabled", "role", "data-vv-as"];
const KEY_ATTRS = ["data-field-id", "field", "name", "id", "type", "placeholder"];

function getAttrs(el) {
    const attrs = {};
    for (const k of ALL_ATTRS) {
        const v = el.getAttribute(k);
        if (v && v !== "null" && v !== "undefined") {
            attrs[k] = k === "class" ? v.substring(0, 80) : v;
        }
    }
    const text = (el.textContent || "").trim().substring(0, 60);
    if (text) attrs._text = text;
    const img = el.querySelector("img[alt]");
    if (img) attrs._img_alt = img.getAttribute("alt");
    return attrs;
}

function suggestXpath(tag, attrs) {
    const dfid = attrs["data-field-id"];
    if (dfid) return "//" + tag + "[@data-field-id='" + dfid + "']";
    const parentDfid = attrs._parent_dfid;
    if (parentDfid) return "//div[@data-field-id='" + parentDfid + "']//" + tag;
    const field = attrs.field;
    if (field && tag === "td") return "//td[@field='" + field + "']";
    const elemId = attrs.id;
    if (elemId && !elemId.startsWith("el-") && elemId.length < 50)
        return "//" + tag + "[@id='" + elemId + "']";
    const name = attrs.name;
    if (name) return "//" + tag + "[@name='" + name + "']";
    const text = (attrs._text || "").trim();
    if (text && (tag === "button" || tag === "a") && text.length < 30) {
        if (/\d/.test(text)) {
            const prefix = text.replace(/[\d,]+\s*$/, "").trim();
            if (prefix) return "//" + tag + "[starts-with(normalize-space(),'" + prefix + "')]";
            return "//" + tag + "[contains(normalize-space(),'" + text.replace(/[\d,\s]+/g, "").trim() + "')]";
        }
        return "//" + tag + "[normalize-space()='" + text + "']";
    }
    const title = attrs.title;
    if (title && title.length < 40) return "//" + tag + "[@title='" + title + "']";
    const cls = attrs["class"];
    if (cls && !["input", "textarea", "select", "button"].includes(tag)) {
        const classes = cls.split(/\s+/).filter(c => c && !c.startsWith("e-") && !c.startsWith("el-"));
        if (classes.length) return "//" + tag + "[contains(@class,'" + classes[0] + "')]";
    }
    return null;
}

const locatorType = arguments[0];
const locatorValue = arguments[1];
let elements;
if (locatorType === "xpath") {
    const snap = document.evaluate(locatorValue, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
    elements = [];
    for (let i = 0; i < snap.snapshotLength; i++) elements.push(snap.snapshotItem(i));
} else {
    elements = Array.from(document.querySelectorAll(locatorValue));
}

return elements.map(function(el) {
    const tag = el.tagName.toLowerCase();
    const attrs = getAttrs(el);
    const xpath = suggestXpath(tag, attrs);
    const disabled = el.disabled === true || el.getAttribute("disabled") !== null;
    const keyParts = [];
    for (const k of KEY_ATTRS) {
        if (attrs[k]) keyParts.push(k + '="' + attrs[k] + '"');
    }
    const rect = el.getBoundingClientRect();
    const visible = rect.width > 0 && rect.height > 0;
    return {
        tag: tag,
        attrs: attrs,
        text: attrs._text || "",
        xpath: xpath,
        keyParts: keyParts.join(" ") || "(no key attrs)",
        enabled: !disabled,
        visible: visible
    };
});
"""


def cmd_find(args):
    driver = _get_driver()
    by, selector = _resolve_locator(args)

    results = driver.execute_script(_FIND_JS, "xpath" if by == By.XPATH else "css", selector)
    total = len(results)
    hidden_count = sum(1 for r in results if not r.get("visible", True))
    print(f"Found {total} element(s):\n")

    for i, item in enumerate(results, 1):
        vis = "visible" if item.get("visible", True) else "HIDDEN"
        status = "enabled" if item["enabled"] else "DISABLED"
        print(f"  #{i}  <{item['tag']}> {item['keyParts']}  [{vis}, {status}]")
        if item["text"]:
            print(f"       text: {item['text']}")
        if item["xpath"]:
            print(f"       -> {item['xpath']}")
        print()

    if total > 1:
        print(
            f"  ⚠️  match={total} (hidden={hidden_count}): Selenium find_element 取 DOM 首個，可能是 hidden。加 scope 限縮到 match=1。"
        )


def _find_dialog_scope(driver, name=None):
    driver.implicitly_wait(0)
    try:
        if name:
            el = driver.execute_script(
                """
                var name = arguments[0];
                var dialogs = document.querySelectorAll('.e-dialog');
                for (var i = dialogs.length - 1; i >= 0; i--) {
                    var title = dialogs[i].querySelector('.e-dlg-header');
                    if (title && title.textContent.trim().includes(name)) return dialogs[i];
                }
                var panels = document.querySelectorAll('.panel-title');
                for (var i = panels.length - 1; i >= 0; i--) {
                    if (panels[i].textContent.trim().includes(name)) {
                        return panels[i].parentElement.parentElement;
                    }
                }
                var elDialogs = document.querySelectorAll('.el-dialog');
                for (var i = elDialogs.length - 1; i >= 0; i--) {
                    var title = elDialogs[i].querySelector('.el-dialog__title');
                    if (title && title.textContent.trim().includes(name)) return elDialogs[i];
                }
                return null;
            """,
                name,
            )
            if el:
                return el
        else:
            topmost = driver.execute_script("""
                var selectors = ['.e-dialog', '.panel.window', '.el-dialog'];
                var best = null;
                var bestZ = -1;
                for (var s = 0; s < selectors.length; s++) {
                    var els = document.querySelectorAll(selectors[s]);
                    for (var i = 0; i < els.length; i++) {
                        var el = els[i];
                        if (el.offsetWidth === 0 && el.offsetHeight === 0) continue;
                        var z = parseInt(window.getComputedStyle(el).zIndex) || 0;
                        if (z > bestZ || (z === bestZ && best === null)) {
                            bestZ = z;
                            best = el;
                        }
                    }
                }
                return best;
            """)
            if topmost:
                return topmost
    finally:
        driver.implicitly_wait(5)
    return None


def cmd_scan(args):
    driver = _get_driver()

    print(f"=== Page Scan ===")
    print(f"URL:   {driver.current_url}")
    print(f"Title: {driver.title}\n")

    scope_selector = None
    if args.dialog is not None:
        scope_el = _find_dialog_scope(driver, args.dialog or None)
        if scope_el:
            scope_selector = _get_scope_css_selector(driver, scope_el)
            print(f"[Scope] dialog: {args.dialog or '(auto-detect)'}\n")
        else:
            print(f"[Scope] dialog not found, scanning full page\n")
    elif args.panel:
        panel_el = driver.execute_script(
            """
            var name = arguments[0];
            var titles = document.querySelectorAll('.panel-title');
            for (var i = 0; i < titles.length; i++) {
                if (titles[i].textContent.trim().includes(name)) {
                    var header = titles[i].closest('.panel-header') || titles[i].parentElement;
                    var next = header.nextElementSibling;
                    var body = (next && next.classList.contains('panel-body')) ? next : null;
                    return body ? [body] : [];
                }
            }
            return [];
        """,
            args.panel,
        )
        if panel_el:
            scope_selector = _get_scope_css_selector(driver, panel_el[0])
            print(f"[Scope] panel: {args.panel}\n")
        else:
            print(f"[Scope] panel '{args.panel}' not found, scanning full page\n")

    result = driver.execute_script(_SCAN_JS, scope_selector, args.hidden, args.all, args.vue)

    fw = result.get("frameworks", {})
    active = [f"{k}({v})" for k, v in fw.items() if v > 0]
    print(f"[Frameworks] {', '.join(active) if active else 'none detected'}\n")

    tag_filter = set(t.lower() for t in (args.tag or []))

    def _filtered(items):
        if not tag_filter:
            return items
        return [it for it in items if it["tag"] in tag_filter]

    total = 0
    for group_name, items in result.get("groups", {}).items():
        filtered = _filtered(items)
        if tag_filter and not filtered:
            continue
        print(f"[{group_name}] ({len(filtered)})")
        for i, item in enumerate(filtered, 1):
            _print_scan_item(i, item)
            total += 1
        print()

    role_items = _filtered(result.get("roles", []))
    if role_items:
        print(f"[Interactive Roles] ({len(role_items)})")
        for i, item in enumerate(role_items, 1):
            _print_scan_item(i, item)
            total += 1
        print()

    clickable_items = _filtered(result.get("clickable", []))
    if clickable_items:
        print(f"[Clickable] ({len(clickable_items)})")
        for i, item in enumerate(clickable_items, 1):
            _print_scan_item(i, item)
            total += 1
        print()

    vue_items = _filtered(result.get("vueComponents", []))
    if vue_items:
        print(f"[Vue Components] ({len(vue_items)})")
        for i, item in enumerate(vue_items, 1):
            _print_scan_item(i, item)
            similar = item.get("_similar_count")
            if similar and similar > 1:
                print(f"       ({similar} similar)")
            total += 1
        print()

    grid_cols = result.get("gridColumns", [])
    if grid_cols:
        print(f"[Grid Columns] ({len(grid_cols)} unique @field values)")
        for i, col in enumerate(grid_cols, 1):
            extras = []
            if col.get("hasInput"):
                extras.append("editable")
            if col.get("hasBtn"):
                extras.append("has-button")
            extra_str = f"  [{', '.join(extras)}]" if extras else ""
            sample = f'  sample="{col["sample"]}"' if col.get("sample") else ""
            print(f"  #{i}  field=\"{col['field']}\"{extra_str}{sample}")
            print(f"       -> //td[@field='{col['field']}']")
            total += 1
        print()

    grid_rows = result.get("gridRows", [])
    if grid_rows:
        print("[Grid Rows]")
        for gr in grid_rows:
            print(f"  {gr['framework']}: {gr['count']} rows  sample: {gr['sampleXpath']}")
        print()

    custom_cards = result.get("customCards")
    if custom_cards:
        print(f"[Custom Cards] {custom_cards['type']}")
        print(f"  {custom_cards['count']} cards  sample: {custom_cards['sampleXpath']}")
        print()

    print(f"Total: {total} interactive elements + {len(grid_cols)} grid columns")


def _get_scope_css_selector(driver, element):
    driver.execute_script(
        "var old = document.getElementById('cli-scope-temp'); "
        "if (old) old.removeAttribute('id');"
    )
    result = driver.execute_script(
        """
        var el = arguments[0];
        if (el.id) return '#' + CSS.escape(el.id);
        if (el.className) {
            var cls = el.className.split(' ').filter(c => c && !c.startsWith('e-')).join('.');
            if (cls) {
                var selector = el.tagName.toLowerCase() + '.' + cls;
                if (document.querySelectorAll(selector).length === 1) return selector;
            }
        }
        return null;
    """,
        element,
    )
    if not result:
        driver.execute_script("arguments[0].id = 'cli-scope-temp'", element)
        result = "#cli-scope-temp"
    return result


def cmd_shot(args):
    driver = _get_driver()
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    name = args.name or f"shot_{int(time.time())}.png"
    if not name.endswith(".png"):
        name += ".png"
    path = SCREENSHOT_DIR / name

    if getattr(args, "xpath", None) or getattr(args, "css", None):
        by, selector = _resolve_locator(args)
        el = driver.find_element(by, selector)
        el.screenshot(str(path))
    else:
        driver.save_screenshot(str(path))
    print(str(path))


_A11Y_JS = """
function buildTree(el, depth) {
    if (depth > 8) return null;
    const role = el.getAttribute("role") || getImplicitRole(el);
    if (!role || role === "generic" || role === "presentation") {
        const children = [];
        for (const child of el.children) {
            const subtree = buildTree(child, depth + 1);
            if (subtree) {
                if (Array.isArray(subtree)) children.push(...subtree);
                else children.push(subtree);
            }
        }
        return children.length ? children : null;
    }

    const name = el.getAttribute("aria-label")
        || el.getAttribute("title")
        || el.getAttribute("data-field-id")
        || getLabel(el)
        || (el.textContent || "").trim().substring(0, 40);
    const state = [];
    if (el.getAttribute("aria-expanded") === "true") state.push("expanded");
    if (el.getAttribute("aria-expanded") === "false") state.push("collapsed");
    if (el.getAttribute("aria-selected") === "true") state.push("selected");
    if (el.getAttribute("aria-disabled") === "true" || el.disabled) state.push("disabled");
    if (el.getAttribute("aria-checked") === "true") state.push("checked");
    if (!el.offsetWidth && !el.offsetHeight) state.push("hidden");

    const result = { role, name: name || "", state, depth, tag: el.tagName.toLowerCase() };
    result.children = [];
    for (const child of el.children) {
        const subtree = buildTree(child, depth + 1);
        if (subtree) {
            if (Array.isArray(subtree)) result.children.push(...subtree);
            else result.children.push(subtree);
        }
    }
    return result;
}

function getImplicitRole(el) {
    const tag = el.tagName.toLowerCase();
    const map = {
        "a": el.hasAttribute("href") ? "link" : null,
        "button": "button",
        "input": el.type === "checkbox" ? "checkbox"
            : el.type === "radio" ? "radio"
            : el.type === "search" ? "searchbox"
            : el.type === "button" || el.type === "submit" ? "button"
            : "textbox",
        "select": "combobox",
        "textarea": "textbox",
        "table": "table",
        "td": "cell",
        "th": "columnheader",
        "tr": "row",
        "thead": "rowgroup",
        "tbody": "rowgroup",
        "ul": "list",
        "ol": "list",
        "li": "listitem",
        "nav": "navigation",
        "main": "main",
        "header": "banner",
        "footer": "contentinfo",
        "aside": "complementary",
        "section": "region",
        "form": "form",
        "fieldset": "group",
        "dialog": "dialog",
        "img": "img",
        "h1": "heading", "h2": "heading", "h3": "heading",
        "h4": "heading", "h5": "heading", "h6": "heading",
    };
    if (map[tag]) return map[tag];
    if (el.classList.contains("e-dialog")) return "dialog";
    if (el.classList.contains("e-grid")) return "grid";
    if (el.classList.contains("datagrid")) return "grid";
    if (el.classList.contains("panel-title")) return "heading";
    if (el.classList.contains("el-dialog")) return "dialog";
    return null;
}

function getLabel(el) {
    const label = el.closest("div")?.previousElementSibling;
    if (label && label.tagName === "LABEL") {
        return (label.getAttribute("title") || label.textContent.trim()).substring(0, 40);
    }
    return null;
}

function flattenTree(node, results, indent) {
    const stateStr = node.state.length ? ` [${node.state.join(", ")}]` : "";
    const nameStr = node.name ? ` "${node.name}"` : "";
    results.push("  ".repeat(indent) + `${node.role}${nameStr}${stateStr}`);
    for (const child of (node.children || [])) {
        flattenTree(child, results, indent + 1);
    }
}

const scopeSelector = arguments[0] || null;
let root = document;
if (scopeSelector) {
    const scopeEl = document.querySelector(scopeSelector);
    if (scopeEl) root = scopeEl;
}

const tree = buildTree(root.body || root, 0);
const lines = [];
if (tree) {
    if (Array.isArray(tree)) tree.forEach(n => flattenTree(n, lines, 0));
    else flattenTree(tree, lines, 0);
}
return lines.join("\\n");
"""


def cmd_a11y(args):
    driver = _get_driver()

    scope_selector = None
    if args.dialog is not None:
        scope_el = _find_dialog_scope(driver, args.dialog or None)
        if scope_el:
            scope_selector = _get_scope_css_selector(driver, scope_el)
            print(f"[Scope] dialog: {args.dialog or '(auto-detect)'}\n")

    print(f"=== Accessibility Tree ===")
    print(f"URL: {driver.current_url}\n")

    result = driver.execute_script(_A11Y_JS, scope_selector)
    print(result)


def cmd_labels(args):
    driver = _get_driver()

    scope_selector = None
    if args.dialog is not None:
        scope_el = _find_dialog_scope(driver, args.dialog or None)
        if scope_el:
            scope_selector = _get_scope_css_selector(driver, scope_el)
            print(f"[Scope] dialog: {args.dialog or '(auto-detect)'}\n")
        else:
            print(f"[Scope] dialog not found, scanning full page\n")
    elif args.panel:
        panel_el = driver.execute_script(
            """
            var name = arguments[0];
            var titles = document.querySelectorAll('.panel-title');
            for (var i = 0; i < titles.length; i++) {
                if (titles[i].textContent.trim().includes(name)) {
                    var header = titles[i].closest('.panel-header') || titles[i].parentElement;
                    var next = header.nextElementSibling;
                    var body = (next && next.classList.contains('panel-body')) ? next : null;
                    return body ? [body] : [];
                }
            }
            return [];
        """,
            args.panel,
        )
        if panel_el:
            scope_selector = _get_scope_css_selector(driver, panel_el[0])
            print(f"[Scope] panel: {args.panel}\n")
        else:
            print(f"[Scope] panel '{args.panel}' not found, scanning full page\n")

    labels = driver.execute_script(
        """
        var scope = arguments[0] ? document.querySelector(arguments[0]) : document;
        if (!scope) scope = document;
        var spans = scope.querySelectorAll('span.truncate');
        var result = [];
        for (var i = 0; i < spans.length; i++) {
            var s = spans[i];
            if (s.offsetParent === null && s.offsetWidth === 0) continue;
            var text = s.textContent.trim();
            if (text) result.push(text);
        }
        return result;
    """,
        scope_selector,
    )

    if not labels:
        print("No labels found.")
        return

    print(f"=== UI Labels ({len(labels)}) ===")
    for i, label in enumerate(labels, 1):
        print(f"  #{i}  {label}")


def cmd_ddl_options(_args):
    driver = _get_driver()
    result = driver.execute_script("""
        // --- Syncfusion EJ2 ---
        var popups = document.querySelectorAll('.e-popup-open');
        var ddlPopup = null;
        for (var i = 0; i < popups.length; i++) {
            var p = popups[i];
            if (p.classList.contains('e-ddl') || p.querySelector('.e-list-parent') || p.querySelector('.e-input-filter')) {
                ddlPopup = p;
                break;
            }
        }
        if (ddlPopup) {
            var filterInput = ddlPopup.querySelector('.e-input-filter');
            var filterValue = filterInput ? filterInput.value : null;
            var items = ddlPopup.querySelectorAll('li');
            var options = [];
            for (var j = 0; j < items.length; j++) {
                var li = items[j];
                if (li.offsetParent === null && li.offsetWidth === 0) continue;
                options.push(li.textContent.trim());
            }
            return {framework: 'syncfusion', filter: filterValue, count: options.length, options: options};
        }

        // --- Element UI ---
        var elDrops = document.querySelectorAll('div.el-select-dropdown');
        var elPopup = null;
        for (var i = 0; i < elDrops.length; i++) {
            var d = elDrops[i];
            if (d.style.display !== 'none' && d.offsetHeight > 0) {
                elPopup = d;
                break;
            }
        }
        if (elPopup) {
            var items = elPopup.querySelectorAll('ul.el-select-dropdown__list > li');
            var options = [];
            for (var j = 0; j < items.length; j++) {
                var li = items[j];
                if (li.offsetParent === null && li.offsetWidth === 0) continue;
                options.push(li.textContent.trim());
            }
            return {framework: 'elementui', filter: null, count: options.length, options: options};
        }

        // --- EasyUI combobox ---
        var comboPanels = document.querySelectorAll('.combo-p');
        var euPopup = null;
        for (var i = 0; i < comboPanels.length; i++) {
            var cp = comboPanels[i];
            if (cp.offsetHeight > 0 && getComputedStyle(cp).display !== 'none') {
                euPopup = cp;
                break;
            }
        }
        if (euPopup) {
            var items = euPopup.querySelectorAll('.combobox-item');
            var options = [];
            for (var j = 0; j < items.length; j++) {
                options.push(items[j].textContent.trim());
            }
            return {framework: 'easyui', filter: null, count: options.length, options: options};
        }

        return {error: 'No open DDL/combobox popup found'};
    """)

    if result.get("error"):
        print(result["error"])
        sys.exit(1)

    framework = result.get("framework", "")
    filter_val = result.get("filter")
    options = result.get("options", [])

    header_parts = [f"{len(options)} items"]
    if framework:
        header_parts.append(framework)
    if filter_val:
        header_parts.append(f'filter: "{filter_val}"')

    print(f"=== DDL Options ({', '.join(header_parts)}) ===")

    for i, opt in enumerate(options, 1):
        print(f"  #{i}  {opt}")


def cmd_js(args):
    driver = _get_driver()
    if args.file:
        code = Path(args.file).read_text(encoding="utf-8")
    else:
        code = args.code
    if not code:
        print("ERROR: Provide JS code or --file", file=sys.stderr)
        sys.exit(1)
    result = driver.execute_script(code)
    if result is not None:
        if isinstance(result, (dict, list)):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result)


def cmd_describe(_args):
    driver = _get_driver()
    info = driver.execute_script("""
        const r = {};
        r.url = location.href;
        r.title = document.title;

        const heading = document.querySelector('.breadcrumb, .page-header, h1, h2');
        r.heading = heading ? heading.textContent.trim().substring(0, 80) : null;

        r.dialogs = [];
        document.querySelectorAll('.e-dialog:not([style*="display: none"]), .el-dialog__wrapper:not([style*="display: none"]), .panel.window:not([style*="display: none"])').forEach(d => {
            const title = d.querySelector('.e-dlg-header, .el-dialog__title, .panel-title');
            const visible = d.offsetWidth > 0 || d.offsetHeight > 0;
            if (visible && title) r.dialogs.push(title.textContent.trim().substring(0, 60));
        });

        r.panels = [];
        document.querySelectorAll('.panel-title').forEach(p => {
            if (p.offsetWidth > 0) r.panels.push(p.textContent.trim().substring(0, 60));
        });

        const activeTab = document.querySelector('.e-tab-header .e-active .e-tab-text, .el-tabs__item.is-active');
        r.activeTab = activeTab ? activeTab.textContent.trim() : null;

        const alert = document.querySelector('.el-message-box, .e-alert, [role="alert"]');
        r.alert = alert && alert.offsetWidth > 0 ? alert.textContent.trim().substring(0, 100) : null;

        var easyuiRows = document.querySelectorAll('tr[datagrid-row-index]');
        var easyuiDedup = new Set(); easyuiRows.forEach(function(r){ easyuiDedup.add(r.getAttribute('datagrid-row-index')); });
        var sfRows = document.querySelectorAll('.e-gridcontent .e-row');
        r.tableRows = easyuiDedup.size + sfRows.length || document.querySelectorAll('table tr').length;

        const pager = document.querySelector('.e-pagercontainer, .pagination-info');
        r.pagination = pager ? pager.textContent.trim().substring(0, 60) : null;

        return r;
    """)

    print(f"URL:   {info.get('url', '')}")
    if info.get("heading"):
        print(f"Page:  {info['heading']}")
    if info.get("dialogs"):
        print(f"Dialogs: {', '.join(info['dialogs'])}")
    if info.get("panels"):
        print(f"Panels:  {', '.join(info['panels'])}")
    if info.get("activeTab"):
        print(f"Tab:   {info['activeTab']}")
    if info.get("alert"):
        print(f"Alert: {info['alert']}")
    if info.get("tableRows"):
        print(f"Table: {info['tableRows']} rows")
    if info.get("pagination"):
        print(f"Pager: {info['pagination']}")


def cmd_grid_headers(_args):
    driver = _get_driver()
    grids = driver.execute_script(r"""
        var result = [];

        // 1. EasyUI DataGrid: .datagrid-header td[field] with visible text
        document.querySelectorAll('.datagrid-view').forEach(function(view, vi) {
            var headers = view.querySelectorAll('.datagrid-header td[field]');
            if (headers.length === 0) return;
            var cols = [];
            headers.forEach(function(h) {
                var text = h.innerText.trim();
                if (text) cols.push(text);
            });
            if (cols.length > 0) {
                result.push({type: 'EasyUI DataGrid', index: vi, columns: cols});
            }
        });

        // 2. Custom table with data-field-id tds: find header row by looking for th or header-style tr
        document.querySelectorAll('table').forEach(function(table, ti) {
            // Skip DataGrid tables (already handled)
            if (table.closest('.datagrid-view')) return;
            var ths = table.querySelectorAll('th');
            if (ths.length === 0) return;
            var cols = [];
            ths.forEach(function(th) {
                var text = th.innerText.trim();
                if (text) cols.push(text);
            });
            if (cols.length > 0) {
                result.push({type: 'Table', index: ti, columns: cols});
            }
        });

        // 3. Syncfusion Grid: .e-gridheader th with text
        document.querySelectorAll('.e-grid').forEach(function(grid, gi) {
            var headers = grid.querySelectorAll('.e-gridheader th .e-headertext');
            if (headers.length === 0) return;
            var cols = [];
            headers.forEach(function(h) {
                var text = h.innerText.trim();
                if (text) cols.push(text);
            });
            if (cols.length > 0) {
                result.push({type: 'Syncfusion Grid', index: gi, columns: cols});
            }
        });

        return result;
    """)

    if not grids:
        print("No grid/table headers found.")
        return

    for g in grids:
        label = f"{g['type']} #{g['index']}"
        cols = " | ".join(g["columns"])
        print(f"[{label}] {cols}")


_DIFF_SNAPSHOT_JS = r"""
var snap = {dialogs:[], panels:[], iframes:[], alert:null, activeTab:null, elements:{}, tableRows:{}};

document.querySelectorAll('.e-dialog:not([style*="display: none"]), .el-dialog__wrapper:not([style*="display: none"]), .panel.window:not([style*="display: none"])').forEach(function(d) {
    var title = d.querySelector('.e-dlg-header, .el-dialog__title, .panel-title');
    if ((d.offsetWidth > 0 || d.offsetHeight > 0) && title)
        snap.dialogs.push(title.textContent.trim().substring(0, 60));
});

document.querySelectorAll('.panel-title').forEach(function(p) {
    if (p.offsetWidth > 0) snap.panels.push(p.textContent.trim().substring(0, 60));
});

var at = document.querySelector('.e-tab-header .e-active .e-tab-text, .el-tabs__item.is-active');
snap.activeTab = at ? at.textContent.trim() : null;

var al = document.querySelector('.el-message-box, .e-alert, [role="alert"]');
snap.alert = (al && al.offsetWidth > 0) ? al.textContent.trim().substring(0, 100) : null;

var tags = ['button', 'input', 'select', 'textarea'];
for (var t = 0; t < tags.length; t++) {
    var els = document.getElementsByTagName(tags[t]);
    for (var i = 0; i < els.length; i++) {
        var el = els[i];
        var dfid = el.getAttribute('data-field-id');
        if (!dfid) {
            var parent = el.closest('[data-field-id]');
            if (parent) dfid = parent.getAttribute('data-field-id');
        }
        if (!dfid) continue;
        var visible = el.offsetWidth > 0 || el.offsetHeight > 0;
        var hasValue = el.value && el.value.trim();
        if (!visible && !hasValue) continue;
        var key = tags[t] + ':' + dfid;
        if (snap.elements[key] && !hasValue) continue;
        var labelEl = parent ? parent.querySelector('label') : null;
        var label = labelEl ? labelEl.textContent.replace(/^\*\s*/, '').trim().substring(0, 20) : '';
        snap.elements[key] = {
            tag: tags[t],
            dfid: dfid,
            label: label,
            disabled: el.disabled || el.hasAttribute('disabled'),
            text: (hasValue ? el.value : (el.textContent || '')).trim().substring(0, 30)
        };
    }
}

var clickables = document.querySelectorAll('span[data-field-id], label[data-field-id], i[data-field-id], a[data-field-id]');
for (var j = 0; j < clickables.length; j++) {
    var c = clickables[j];
    if (c.offsetWidth === 0 && c.offsetHeight === 0) continue;
    var cdfid = c.getAttribute('data-field-id');
    var tdParent = c.closest('td[data-field-id]');
    var tdDfid = (tdParent && tdParent !== c) ? tdParent.getAttribute('data-field-id') : null;
    var ckey = (tdDfid ? tdDfid + ':' : '') + c.tagName.toLowerCase() + ':' + cdfid;
    if (snap.elements[ckey]) continue;
    snap.elements[ckey] = {
        tag: c.tagName.toLowerCase(),
        dfid: cdfid,
        tdDfid: tdDfid,
        disabled: false,
        text: (c.textContent || '').trim().substring(0, 30)
    };
}

snap.checkboxes = [];
document.querySelectorAll('.el-checkbox').forEach(function(cb) {
    if (cb.offsetWidth === 0) return;
    var label = cb.textContent.trim().substring(0, 30);
    snap.checkboxes.push('el|' + label + '|' + cb.classList.contains('is-checked'));
});
document.querySelectorAll('input[type="checkbox"]:not(.el-checkbox__original)').forEach(function(cb, i) {
    if (cb.offsetWidth === 0 && cb.offsetHeight === 0) return;
    var name = cb.name || cb.id || 'cb';
    snap.checkboxes.push('html|' + name + '#' + (i+1) + '|' + cb.checked);
});

snap.tableRows = {
    easyui: (function(){ var rs=document.querySelectorAll('tr[datagrid-row-index]'); var s=new Set(); rs.forEach(function(r){s.add(r.getAttribute('datagrid-row-index'))}); return s.size; })(),
    syncfusion: document.querySelectorAll('.e-gridcontent .e-row').length,
    total: document.querySelectorAll('table tr').length,
    selectedIds: Array.from(document.querySelectorAll('tr.datagrid-row-selected, .e-row.e-active, .e-row.my-row-selected')).map(function(r){return r.id || r.getAttribute('data-uid') || ''}).filter(function(id){return id}).join(',')
};

var popups = document.querySelectorAll('.e-popup-open, .el-picker-panel, .el-select-dropdown');
snap.popups = Array.from(popups).filter(function(p) { return p.offsetWidth > 0 || p.offsetHeight > 0; }).length;

document.querySelectorAll('iframe').forEach(function(f) {
    if (f.offsetWidth === 0 && f.offsetHeight === 0) return;
    var id = f.id || f.name || '';
    var src = (f.src || '').substring(0, 80);
    if (id || src) snap.iframes.push({id: id, src: src});
});

return snap;
"""


def _print_failure_diagnostics(driver, element=None):
    """Print current page state for click/type failure diagnostics."""
    if element:
        el_state = driver.execute_script(
            """
            var el = arguments[0];
            var r = [];
            if (el.disabled) r.push("disabled");
            if (el.readOnly) r.push("readonly");
            if (el.offsetWidth === 0 || el.offsetHeight === 0) r.push("hidden(0x0)");
            var s = window.getComputedStyle(el);
            if (s.visibility === 'hidden') r.push("visibility:hidden");
            if (s.display === 'none') r.push("display:none");
            if (s.pointerEvents === 'none') r.push("pointer-events:none");
            var tag = el.tagName.toLowerCase();
            var type = el.type || '';
            return {reasons: r, tag: tag, type: type};
        """,
            element,
        )
        if el_state:
            reasons = el_state.get("reasons", [])
            tag = el_state.get("tag", "?")
            etype = el_state.get("type", "")
            label = f"{tag}" + (f"[{etype}]" if etype else "")
            if reasons:
                print(f"  Element <{label}> is: {', '.join(reasons)}")
            else:
                print(f"  Element <{label}> appears normal (not disabled/hidden)")
    snap = driver.execute_script(_DIFF_SNAPSHOT_JS)
    parts = []
    if snap.get("alert"):
        parts.append(f"ALERT: {snap['alert'][:80]}")
    if snap.get("dialogs"):
        parts.append(f"Dialogs: {', '.join(snap['dialogs'])}")
    if snap.get("panels"):
        parts.append(f"Panels: {', '.join(snap['panels'])}")
    if snap.get("popups"):
        parts.append(f"Popups: {snap['popups']}")
    if parts:
        print("  Current state:")
        for p in parts:
            print(f"    {p}")


def _diff_compare(baseline, current):
    """Compare two snapshots and print changes. Returns True if changes found."""
    changes = []

    for kind in ["dialogs", "panels"]:
        old_set = set(baseline.get(kind, []))
        new_set = set(current.get(kind, []))
        for item in new_set - old_set:
            changes.append(("NEW", kind[:-1], item))
        for item in old_set - new_set:
            changes.append(("GONE", kind[:-1], item))

    if baseline.get("alert") != current.get("alert"):
        if current.get("alert"):
            changes.append(("ALERT", "", current["alert"]))
        elif baseline.get("alert"):
            changes.append(("ALERT_GONE", "", baseline["alert"]))

    if baseline.get("activeTab") != current.get("activeTab"):
        changes.append(("TAB", f"{baseline.get('activeTab')} → {current.get('activeTab')}", ""))

    old_rows = baseline.get("tableRows", {})
    new_rows = current.get("tableRows", {})
    for grid_type in ["easyui", "syncfusion", "total"]:
        old_count = old_rows.get(grid_type, 0)
        new_count = new_rows.get(grid_type, 0)
        if old_count != new_count:
            diff_val = new_count - old_count
            sign = "+" if diff_val > 0 else ""
            changes.append(("ROWS", grid_type, f"{old_count} → {new_count} ({sign}{diff_val})"))

    old_sel = old_rows.get("selectedIds", "")
    new_sel = new_rows.get("selectedIds", "")
    if old_sel != new_sel:
        old_ids = set(old_sel.split(",")) if old_sel else set()
        new_ids = set(new_sel.split(",")) if new_sel else set()
        picked = new_ids - old_ids
        dropped = old_ids - new_ids

        def _short(ids):
            return ", ".join(sorted(i.split("-r")[-1] if "-r" in i else i for i in ids))

        parts = []
        if picked:
            parts.append(f"selected row {_short(picked)}")
        if dropped:
            parts.append(f"deselected row {_short(dropped)}")
        changes.append(("SELECTION", "grid", ", ".join(parts) if parts else "changed"))

    old_popups = baseline.get("popups", 0)
    new_popups = current.get("popups", 0)
    if old_popups != new_popups:
        diff_val = new_popups - old_popups
        sign = "+" if diff_val > 0 else ""
        changes.append(
            ("POPUPS", "dropdown/popup", f"{old_popups} → {new_popups} ({sign}{diff_val})")
        )

    old_cbs = {}
    for s in baseline.get("checkboxes", []):
        parts = s.split("|", 2)
        if len(parts) == 3:
            old_cbs[parts[1]] = parts[2] == "true"
    new_cbs = {}
    for s in current.get("checkboxes", []):
        parts = s.split("|", 2)
        if len(parts) == 3:
            new_cbs[parts[1]] = parts[2] == "true"
    for name in new_cbs:
        if name not in old_cbs:
            state = "checked" if new_cbs[name] else "unchecked"
            changes.append(("CHECKBOX", name, f"NEW {state}"))
        elif old_cbs[name] != new_cbs[name]:
            state = "checked" if new_cbs[name] else "unchecked"
            changes.append(("CHECKBOX", name, state))

    old_iframes = {f.get("id") or str(i): f for i, f in enumerate(baseline.get("iframes", []))}
    new_iframes = {f.get("id") or str(i): f for i, f in enumerate(current.get("iframes", []))}
    for key in new_iframes:
        if key not in old_iframes:
            changes.append(("NEW", "iframe", key))
        else:
            old_src = old_iframes[key].get("src", "")
            new_src = new_iframes[key].get("src", "")
            if old_src != new_src:
                changes.append(("IFRAME", key, f"src changed"))
    for key in old_iframes:
        if key not in new_iframes:
            changes.append(("GONE", "iframe", key))

    old_els = baseline.get("elements", {})
    new_els = current.get("elements", {})

    enabled_list = []
    disabled_list = []

    value_changes = []

    for key in new_els:
        el = new_els[key]
        if key not in old_els:
            td_ctx = f" (in {el['tdDfid']})" if el.get("tdDfid") else ""
            changes.append(("NEW", el["tag"], el["dfid"] + td_ctx))
        else:
            old_el = old_els[key]
            if old_el["disabled"] and not el["disabled"]:
                enabled_list.append(el["dfid"])
            elif not old_el["disabled"] and el["disabled"]:
                disabled_list.append(el["dfid"])
            old_text = old_el.get("text", "")
            new_text = el.get("text", "")
            if old_text != new_text:
                value_changes.append(
                    (el["dfid"], el.get("tag", ""), el.get("label", ""), old_text, new_text)
                )

    for key in old_els:
        if key not in new_els:
            el = old_els[key]
            td_ctx = f" (in {el['tdDfid']})" if el.get("tdDfid") else ""
            changes.append(("GONE", el["tag"], el["dfid"] + td_ctx))

    if not changes and not enabled_list and not disabled_list and not value_changes:
        print("No changes detected.")
        return False

    print("[Changes]")
    for kind, tag, detail in changes:
        if kind == "ALERT":
            print(f"  ALERT:   {detail}")
        elif kind == "ALERT_GONE":
            print(f"  ALERT cleared")
        elif kind == "TAB":
            print(f"  TAB:     {tag}")
        elif kind == "ROWS":
            print(f"  ROWS:    {tag} grid {detail}")
        elif kind == "IFRAME":
            print(f"  IFRAME:  {tag} {detail}")
        elif kind == "SELECTION":
            print(f"  SELECTION grid:{detail}")
        elif kind == "CHECKBOX":
            print(f"  CHECKBOX {tag}: {detail}")
        else:
            label = f"{tag}:{detail}" if detail else tag
            print(f"  {kind:8s} {label}")

    if enabled_list:
        print(f"  ENABLED: {', '.join(enabled_list[:10])}", end="")
        if len(enabled_list) > 10:
            print(f"  (+{len(enabled_list) - 10} more)", end="")
        print()

    if disabled_list:
        print(f"  DISABLED: {', '.join(disabled_list[:10])}", end="")
        if len(disabled_list) > 10:
            print(f"  (+{len(disabled_list) - 10} more)", end="")
        print()

    _DFID_DISPLAY = {"doSearch": "查詢", "doClear": "清除", "doSave": "儲存", "doDelete": "刪除"}

    if value_changes:
        print(f"  VALUES:  ({len(value_changes)} field{'s' if len(value_changes) > 1 else ''})")
        for dfid, tag, label, old_v, new_v in value_changes[:15]:
            old_display = old_v if old_v else "(empty)"
            new_display = new_v if new_v else "(empty)"
            display_dfid = dfid
            if dfid.startswith("undefined_"):
                action = dfid[len("undefined_") :]
                display_dfid = _DFID_DISPLAY.get(action, action)
            name = f"{display_dfid} [{label}]" if label else display_dfid
            print(f"    {name} ({tag}): {old_display} → {new_display}")
        if len(value_changes) > 15:
            print(f"    (+{len(value_changes) - 15} more)")

    return True


def _with_diff(driver, action_fn, wait_seconds=0):
    """Wrap an action with before/after diff snapshots."""
    baseline = driver.execute_script(_DIFF_SNAPSHOT_JS)
    action_fn()

    if wait_seconds > 0:
        stable_count = 0
        stable_target = 3
        current = None
        deadline = time.time() + wait_seconds
        while time.time() < deadline:
            time.sleep(0.5)
            snap = driver.execute_script(_DIFF_SNAPSHOT_JS)
            if snap != baseline:
                current = snap
                stable_count = 0
            elif current is not None:
                stable_count += 1
                if stable_count >= stable_target:
                    break
        if current is None:
            current = driver.execute_script(_DIFF_SNAPSHOT_JS)
    else:
        time.sleep(0.3)
        current = driver.execute_script(_DIFF_SNAPSHOT_JS)

    _diff_compare(baseline, current)


def cmd_diff(_args):
    driver = _get_driver()
    current = driver.execute_script(_DIFF_SNAPSHOT_JS)

    if not DIFF_SNAPSHOT_FILE.exists():
        DIFF_SNAPSHOT_FILE.write_text(json.dumps(current, ensure_ascii=False), encoding="utf-8")
        count = len(current.get("elements", {}))
        dialogs = current.get("dialogs", [])
        panels = current.get("panels", [])
        rows = current.get("tableRows", {})
        tab = current.get("activeTab")
        print(f"Baseline saved: {count} elements, {len(dialogs)} dialogs")
        if dialogs:
            print(f"  Dialogs: {', '.join(dialogs)}")
        if panels:
            print(f"  Panels: {', '.join(panels)}")
        if tab:
            print(f"  Active tab: {tab}")
        row_parts = []
        if rows.get("easyui"):
            row_parts.append(f"EasyUI {rows['easyui']}")
        if rows.get("syncfusion"):
            row_parts.append(f"Syncfusion {rows['syncfusion']}")
        if rows.get("total"):
            row_parts.append(f"total {rows['total']}")
        if rows.get("selected"):
            row_parts.append(f"selected {rows['selected']}")
        if row_parts:
            print(f"  Table rows: {', '.join(row_parts)}")
        print("Run operations, then 'diff' again to see changes.")
        return

    baseline = json.loads(DIFF_SNAPSHOT_FILE.read_text(encoding="utf-8"))
    DIFF_SNAPSHOT_FILE.unlink()
    _diff_compare(baseline, current)


def cmd_source(args):
    driver = _get_driver()
    src = driver.page_source
    path = Path(args.file) if args.file else (SCREENSHOT_DIR.parent / "page_source.html")
    path.parent.mkdir(exist_ok=True)
    path.write_text(src, encoding="utf-8")
    print(f"Saved: {path} ({len(src)} chars)")


def cmd_url(_args):
    print(_get_driver().current_url)


def cmd_title(_args):
    print(_get_driver().title)


def cmd_wait(args):
    driver = _get_driver()
    by, selector = _resolve_locator(args)

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    try:
        WebDriverWait(driver, args.timeout).until(EC.presence_of_element_located((by, selector)))
        print(f"Found: {selector}")
    except Exception:
        print(f"Timeout ({args.timeout}s): {selector}", file=sys.stderr)
        sys.exit(1)


def cmd_tabs(_args):
    driver = _get_driver()
    current = driver.current_window_handle
    for i, h in enumerate(driver.window_handles):
        try:
            driver.switch_to.window(h)
            title = driver.title[:50]
        except WebDriverException:
            title = "(inaccessible)"
        marker = " <- current" if h == current else ""
        print(f"  [{i}] {title}{marker}")
    driver.switch_to.window(current)


def cmd_switch(args):
    driver = _get_driver()
    handles = driver.window_handles
    if args.index < 0 or args.index >= len(handles):
        print(f"ERROR: Index {args.index} out of range (0-{len(handles) - 1})", file=sys.stderr)
        sys.exit(1)
    driver.switch_to.window(handles[args.index])
    print(f"Tab [{args.index}]: {driver.current_url}")


def cmd_hover(args):
    driver = _get_driver()
    by, selector = _resolve_locator(args)
    el = driver.find_element(by, selector)
    from selenium.webdriver.common.action_chains import ActionChains

    ActionChains(driver).move_to_element(el).perform()
    print(f"Hovered: {selector}")


def cmd_get(args):
    driver = _get_driver()
    by, selector = _resolve_locator(args)
    el = driver.find_element(by, selector)

    tag = el.tag_name.lower()
    if tag in ("input", "textarea"):
        value = el.get_attribute("value")
        print(value if value is not None else "")
    elif tag == "select":
        from selenium.webdriver.support.ui import Select

        sel = Select(el)
        try:
            print(sel.first_selected_option.text)
        except NoSuchElementException:
            print("")
    else:
        text = el.text or el.get_attribute("textContent") or ""
        print(text.strip())
    _save_last_op("get", by, selector)


def cmd_pom_out(args):
    if args.show:
        if POM_OUTPUT_FILE.exists():
            print(POM_OUTPUT_FILE.read_text(encoding="utf-8"))
        else:
            print("(empty - no pom_output.py yet)")
        return

    if args.clear:
        if POM_OUTPUT_FILE.exists():
            POM_OUTPUT_FILE.unlink()
        print("Cleared pom_output.py")
        return

    if args.init:
        from datetime import date

        lines = ["# === pom-out 暫存 ==="]
        if args.case:
            title = f" {args.title}" if args.title else ""
            lines.append(f"# Case #{args.case}:{title}")
        lines.append(f"# Generated: {date.today()}")
        lines.append("")
        lines.append("# --- Locators ---")
        lines.append("from selenium.webdriver.common.by import By")
        lines.append("")
        lines.append("# --- Page Methods ---")
        lines.append("")
        POM_OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
        print(f"Initialized pom_output.py" + (f" (Case #{args.case})" if args.case else ""))
        return

    if not args.names:
        print("ERROR: base_name required (or use --init/--show/--clear)", file=sys.stderr)
        sys.exit(1)

    if not LAST_OP_FILE.exists():
        print("ERROR: No last operation. Run click/type/get first.", file=sys.stderr)
        sys.exit(1)

    last_op = json.loads(LAST_OP_FILE.read_text(encoding="utf-8"))
    op_type = last_op["op_type"]
    by_name = last_op["by"]
    selector = last_op["selector"]

    PREFIX = {"click": ("btn_", "click_"), "type": ("input_", "input_"), "get": ("text_", "get_")}

    if len(args.names) == 1:
        base = args.names[0]
        loc_prefix, meth_prefix = PREFIX.get(op_type, ("", ""))
        loc_name = f"{loc_prefix}{base}"
        meth_name = f"{meth_prefix}{base}"
    else:
        loc_name = args.names[0]
        meth_name = args.names[1]

    if '"' in selector:
        locator_line = f"{loc_name} = (By.{by_name}, '{selector}')"
    else:
        locator_line = f'{loc_name} = (By.{by_name}, "{selector}")'

    if op_type == "click":
        method = (
            f"def {meth_name}(self):\n"
            f"    self.click(self.locator.{loc_name})\n"
            f"    return self"
        )
    elif op_type == "type":
        method = (
            f"def {meth_name}(self, value):\n"
            f"    self.input_with_clear(self.locator.{loc_name}, value)\n"
            f"    return self"
        )
    elif op_type == "get":
        method = (
            f"def {meth_name}(self):\n"
            f"    return self.driver.find_element(*self.locator.{loc_name}).get_attribute('value')"
        )
    else:
        print(f"ERROR: Unknown operation type: {op_type}", file=sys.stderr)
        sys.exit(1)

    if POM_OUTPUT_FILE.exists():
        content = POM_OUTPUT_FILE.read_text(encoding="utf-8")
    else:
        content = ""

    if "# --- Page Methods ---" in content:
        parts = content.split("# --- Page Methods ---", 1)
        new_content = (
            parts[0].rstrip()
            + "\n"
            + locator_line
            + "\n\n"
            + "# --- Page Methods ---"
            + parts[1].rstrip()
            + "\n\n"
            + method
            + "\n"
        )
    else:
        new_content = content.rstrip() + f"\n\n{locator_line}\n\n{method}\n"

    POM_OUTPUT_FILE.write_text(new_content, encoding="utf-8")
    print(f"Added: {loc_name} ({op_type}) → pom_output.py")


def cmd_login(args):
    import urllib.parse

    driver = _get_driver()

    base_url = args.base_url or _read_pytest_ini("BASE_URL")
    redirect_url = args.redirect_url or _read_pytest_ini("REDIRECT_URL")
    username = args.username or _read_pytest_ini("USERNAME")
    password = args.password or _read_pytest_ini("PASSWORD")
    client_id = args.client_id
    language = args.language or _read_pytest_ini("LANGUAGE") or "zh-TW"

    for name, val in [
        ("username", username),
        ("password", password),
        ("base_url", base_url),
        ("redirect_url", redirect_url),
    ]:
        if not val:
            print(
                f"ERROR: --{name.replace('_', '-')} not provided and not found in pytest.ini",
                file=sys.stderr,
            )
            sys.exit(1)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": "openid offline_access",
        "redirect_uri": redirect_url,
        "ui_locales": language,
    }
    login_url = f"{base_url}?{urllib.parse.urlencode(params)}"

    print(f"Navigating to login page...", flush=True)
    old_heading = driver.execute_script(
        "return document.querySelector('.breadcrumb, .page-header, h1, h2')"
        "?.textContent?.trim()?.substring(0, 80)"
    )
    driver.get(login_url)
    _wait_for_page(driver, old_heading)
    time.sleep(1)

    username_el = driver.find_element(
        By.XPATH, "//input[@placeholder='使用者名稱'] | //input[@placeholder='使用者']"
    )
    username_el.send_keys(username)
    password_el = driver.find_element(By.XPATH, "//input[@placeholder='密碼']")
    password_el.send_keys(password)

    try:
        import ddddocr
    except ImportError:
        print("ERROR: ddddocr not installed. Run: uv pip install ddddocr", file=sys.stderr)
        sys.exit(1)

    ocr = ddddocr.DdddOcr(show_ad=False)
    max_retries = 30

    for retry in range(max_retries):
        driver.implicitly_wait(0)
        try:
            captcha_el = driver.find_element(By.XPATH, "//img[@id='captchaImg']")
        except NoSuchElementException:
            print("No captcha found, attempting login without it...", flush=True)
            break
        finally:
            driver.implicitly_wait(5)

        try:
            captcha_el.click()
            time.sleep(2)
            captcha_path = SCREENSHOT_DIR / "captcha_login.png"
            SCREENSHOT_DIR.mkdir(exist_ok=True)
            captcha_el.screenshot(str(captcha_path))
        except StaleElementReferenceException:
            print(f"  Retry {retry + 1}: captcha element stale, re-locating...", flush=True)
            continue

        with open(captcha_path, "rb") as f:
            captcha_text = ocr.classification(f.read()).strip()

        verify_el = driver.find_element(By.XPATH, "//input[@placeholder='驗證碼']")
        verify_el.clear()
        verify_el.send_keys(captcha_text)

        login_btn = driver.find_element(By.XPATH, "//button[@id='kc-login'] | //a[@id='login_btn']")
        login_btn.click()
        time.sleep(2)

        current_url = driver.current_url
        still_on_auth = "protocol/openid-connect/auth" in current_url

        if still_on_auth:
            # Still on login page — check for login errors
            wrong_hint = driver.find_elements(By.XPATH, "//span[text()='驗證碼錯誤']")
            if wrong_hint:
                print(f"  Retry {retry + 1}: wrong captcha '{captcha_text}'", flush=True)
                continue

            dialog_btn = driver.find_elements(
                By.XPATH, "//div[@role='dialog' and @aria-label='提示']//button/span"
            )
            if dialog_btn:
                dialog_btn[0].click()
                time.sleep(0.5)
                print(f"  Retry {retry + 1}: dialog dismissed", flush=True)
                continue

            print(f"  Retry {retry + 1}: still on auth page, unrecognized state", flush=True)
            continue

        # URL left auth page — login accepted
        print(f"Login successful! ({retry + 1} attempt(s))", flush=True)
        print(f"URL: {current_url}", flush=True)

        driver.implicitly_wait(0)
        company_links = driver.find_elements(
            By.XPATH, "//h3[contains(text(),'請選擇公司別')]/following::a"
        )
        driver.implicitly_wait(5)
        if company_links:
            target = args.company or company_links[-1].text.split("\n")[0]
            for link in company_links:
                if target in link.text:
                    link.click()
                    print(f"Company selected: {target}", flush=True)
                    time.sleep(3)
                    break
            else:
                company_links[-1].click()
                print(f"Company '{target}' not found, selected last option", flush=True)
                time.sleep(3)

        cookies = driver.get_cookies()
        session_storage = driver.execute_script("""
            let data = {};
            for (let [key, value] of Object.entries(sessionStorage)) {
                data[key] = value;
            }
            return data;
        """)
        existing = {}
        if SESSION_FILE.exists():
            try:
                existing = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                pass
        existing.update(
            {"cookies": cookies, "session_storage": session_storage, "url": driver.current_url}
        )
        SESSION_FILE.write_text(
            json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        PROJECT_SESSION_FILE.write_text(
            json.dumps(session_storage, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(
            f"Session saved ({len(cookies)} cookies + {len(session_storage)} sessionStorage)",
            flush=True,
        )
        return

    print("Login failed after max retries", file=sys.stderr)
    sys.exit(1)


# ─── Argument Parsing ────────────────────────────────────────────


def _add_locator_args(parser, required=True):
    g = parser.add_mutually_exclusive_group(required=required)
    g.add_argument("--xpath", "-x")
    g.add_argument("--css", "-c")
    g.add_argument("--xpath-file", "-xf", help="Read XPath from file (avoids shell quoting)")


def main():
    parser = argparse.ArgumentParser(
        prog="selenium-cli",
        description="Browser automation CLI for Athena PMS locator discovery",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("connect", help="Start browser session")
    p.add_argument("--hub", help="Selenium Hub URL (default: $SELENIUM_HUB)")
    p.add_argument("--edge", action="store_true", help="Use Edge instead of Chrome")
    p.set_defaults(func=cmd_connect)

    p = sub.add_parser("attach", help="Attach to existing browser (needs --remote-debugging-port)")
    p.add_argument("--port", type=int, default=9222, help="Debug port (default: 9222)")
    p.add_argument("--edge", action="store_true", help="Use Edge instead of Chrome")
    p.set_defaults(func=cmd_attach)

    sub.add_parser("close", help="End session").set_defaults(func=cmd_close)

    sub.add_parser(
        "save-session", help="Save browser cookies + sessionStorage to file"
    ).set_defaults(func=cmd_save_browser_session)

    sub.add_parser(
        "restore-session", help="Restore browser cookies + sessionStorage from file"
    ).set_defaults(func=cmd_restore_browser_session)

    p = sub.add_parser("nav", help="Navigate to URL (auto-waits for page load)")
    p.add_argument("url")
    p.add_argument("--no-wait", action="store_true", help="Skip auto-wait")
    p.set_defaults(func=cmd_nav)

    sub.add_parser("back", help="Go back").set_defaults(func=cmd_back)

    p = sub.add_parser("click", help="Click element")
    _add_locator_args(p)
    p.add_argument("--js", action="store_true", help="Force JavaScript click (bypass native click)")
    p.add_argument("--diff", action="store_true", help="Auto diff before/after click")
    p.add_argument(
        "--wait",
        type=int,
        default=0,
        metavar="SEC",
        help="With --diff: wait up to SEC seconds for changes (explicit wait)",
    )
    p.set_defaults(func=cmd_click)

    p = sub.add_parser("type", help="Type text into element")
    _add_locator_args(p)
    p.add_argument("--text", "-t", required=True)
    p.add_argument("--append", action="store_true", help="Append instead of clearing")
    p.add_argument("--enter", action="store_true", help="Press Enter after typing")
    p.set_defaults(func=cmd_type)

    p = sub.add_parser("key", help="Send special key (enter/tab/escape/...)")
    p.add_argument("key_name", metavar="key")
    _add_locator_args(p, required=False)
    p.set_defaults(func=cmd_key, key=None)

    p = sub.add_parser("text", help="Get element text")
    _add_locator_args(p)
    p.set_defaults(func=cmd_text)

    p = sub.add_parser("attr", help="Get element attribute")
    _add_locator_args(p)
    p.add_argument("--name", "-n", required=True, help="Attribute name")
    p.set_defaults(func=cmd_attr)

    p = sub.add_parser("find", help="Find elements, show attributes")
    _add_locator_args(p)
    p.set_defaults(func=cmd_find)

    p = sub.add_parser("scan", help="Scan page for interactive elements")
    p.add_argument("--panel", "-p", help="Scope to panel by title")
    p.add_argument(
        "--dialog", "-d", nargs="?", const="", help="Scope to dialog (name or auto-detect)"
    )
    p.add_argument("--all", "-a", action="store_true", help="Include links & labels")
    p.add_argument("--hidden", action="store_true", help="Include hidden elements")
    p.add_argument(
        "--tag", "-t", action="append", help="Filter by tag type (e.g. button, input, span)"
    )
    p.add_argument(
        "--vue",
        action="store_true",
        help="Include Vue custom components (data-v-* with pointer cursor)",
    )
    p.set_defaults(func=cmd_scan)

    sub.add_parser("describe", help="Text summary of page state").set_defaults(func=cmd_describe)

    sub.add_parser("grid-headers", help="List all grid/table column headers").set_defaults(
        func=cmd_grid_headers
    )
    sub.add_parser(
        "ddl-options", help="List options in the currently open DDL/combobox popup"
    ).set_defaults(func=cmd_ddl_options)

    p = sub.add_parser("labels", help="List UI labels (span.truncate text)")
    p.add_argument("--panel", "-p", help="Scope to panel by title")
    p.add_argument(
        "--dialog", "-d", nargs="?", const="", help="Scope to dialog (name or auto-detect)"
    )
    p.set_defaults(func=cmd_labels)

    sub.add_parser(
        "diff", help="Snapshot/diff page state (run twice: baseline then compare)"
    ).set_defaults(func=cmd_diff)

    p = sub.add_parser("shot", help="Take screenshot")
    p.add_argument("--name", "-n", help="Filename")
    _add_locator_args(p, required=False)
    p.set_defaults(func=cmd_shot)

    p = sub.add_parser("js", help="Execute JavaScript")
    p.add_argument("code", nargs="?", default=None)
    p.add_argument("--file", "-f", help="Read JS from file")
    p.set_defaults(func=cmd_js)

    p = sub.add_parser("source", help="Save page source to file")
    p.add_argument("--file", "-f", help="Output path")
    p.set_defaults(func=cmd_source)

    sub.add_parser("url", help="Print current URL").set_defaults(func=cmd_url)
    sub.add_parser("title", help="Print page title").set_defaults(func=cmd_title)

    p = sub.add_parser("wait", help="Wait for element")
    _add_locator_args(p)
    p.add_argument("--timeout", type=int, default=10)
    p.set_defaults(func=cmd_wait)

    sub.add_parser("tabs", help="List browser tabs").set_defaults(func=cmd_tabs)

    p = sub.add_parser("switch", help="Switch to tab by index")
    p.add_argument("index", type=int)
    p.set_defaults(func=cmd_switch)

    p = sub.add_parser("hover", help="Hover over element")
    _add_locator_args(p)
    p.set_defaults(func=cmd_hover)

    p = sub.add_parser("get", help="Get element text or value")
    _add_locator_args(p)
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("a11y", help="Accessibility tree view")
    p.add_argument("--dialog", "-d", nargs="?", const="", help="Scope to dialog")
    p.set_defaults(func=cmd_a11y)

    p = sub.add_parser("pom-out", help="Output verified locator + page method to pom_output.py")
    p.add_argument(
        "names", nargs="*", help="base_name (auto-prefix) or locator_name method_name (override)"
    )
    p.add_argument("--init", action="store_true", help="Initialize pom_output.py with header")
    p.add_argument("--case", type=int, help="Case ID for header (with --init)")
    p.add_argument("--title", help="Case title for header (with --init)")
    p.add_argument("--show", action="store_true", help="Show current pom_output.py content")
    p.add_argument("--clear", action="store_true", help="Clear pom_output.py")
    p.set_defaults(func=cmd_pom_out)

    p = sub.add_parser("login", help="Login to Athena PMS (reads defaults from pytest.ini)")
    p.add_argument("--username", "-u", help="Username (default: pytest.ini USERNAME)")
    p.add_argument("--password", "-p", help="Password (default: pytest.ini PASSWORD)")
    p.add_argument("--base-url", help="Auth base URL (default: pytest.ini BASE_URL)")
    p.add_argument("--redirect-url", help="Redirect URL (default: pytest.ini REDIRECT_URL)")
    p.add_argument("--client-id", default="internal")
    p.add_argument("--language", default="zh-TW")
    p.add_argument("--company", help="Company name to select (skip if not present)")
    p.set_defaults(func=cmd_login)

    args = parser.parse_args()

    if args.command == "key":
        args.key = args.key_name

    try:
        args.func(args)
    except NoSuchElementException as e:
        print(f"ERROR: Element not found - {e.msg}", file=sys.stderr)
        sys.exit(1)
    except WebDriverException as e:
        msg = getattr(e, "msg", str(e))
        if "invalid session" in msg.lower() or "no such session" in msg.lower():
            print(
                f"ERROR: Session expired. Run 'connect' or 'attach' again.\n{msg}", file=sys.stderr
            )
        else:
            print(f"ERROR: {msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
