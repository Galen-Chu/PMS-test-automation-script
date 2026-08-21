import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

_DATA_CACHE = {}
_TESTS_DIR = Path(__file__).parent.parent / "tests"


def _load_data():
    if not _DATA_CACHE:
        data_path = Path(__file__).parent.parent / "tests" / "test_data.json"
        with open(data_path, encoding="utf-8") as f:
            _DATA_CACHE.update(json.load(f))
    return _DATA_CACHE


def _get_group(group_name: str, env: str = None) -> dict:
    if env is None:
        env = os.getenv("ENV", "autotest")
    data = _load_data()
    return data["environments"][env]["groups"][group_name]


def get_system_date(env: str = None) -> datetime:
    if env is None:
        env = os.getenv("ENV", "autotest")
    data = _load_data()
    date_str = data["environments"][env].get("system_date", "2024/01/05")
    return datetime.strptime(date_str, "%Y/%m/%d")


def resolve_date(offset: str, env: str = None) -> str:
    """相對日期轉實際日期字串。

    Usage:
        resolve_date("+0")  # => "2024/01/05"（system_date 當天）
        resolve_date("+1")  # => "2024/01/06"
        resolve_date("+30") # => "2024/02/04"
        resolve_date("2024/01/05") # => "2024/01/05"（絕對日期直接回傳）
    """
    if not offset.startswith("+") and not offset.startswith("-"):
        return offset
    base = get_system_date(env)
    days = int(offset)
    return (base + timedelta(days=days)).strftime("%Y/%m/%d")


def get_group_data(group_name: str, env: str = None) -> dict:
    """取得指定 group 的 common 資料。日期欄位自動 resolve。"""
    group = _get_group(group_name, env)
    result = dict(group["common"])
    for key in ("checkin_date", "checkout_date"):
        if key in result:
            result[key] = resolve_date(result[key], env)
    return result


def get_test_data(group_name: str, test_key: str, env: str = None) -> dict:
    """取得指定案例的完整資料（common 合併 test-specific）。

    Usage:
        data = get_test_data("test_maindesk_flow_b", "assign_deposit")
        # => {"card_name": "Card Maindesk FLow B", "room": "205", ..., "deposit_nos": "2204"}
    """
    group = _get_group(group_name, env)
    merged = dict(group["common"])
    for item in group.get("tests", []):
        if item.get("key") == test_key:
            specific = {k: v for k, v in item.items() if k != "key"}
            merged.update(specific)
            break
    for key in ("checkin_date", "checkout_date"):
        if key in merged:
            merged[key] = resolve_date(merged[key], env)
    return merged


_GROUP_RE = re.compile(r'@pytest\.mark\.xdist_group\(["\'](.+?)["\']\)')
_DEP_RE = re.compile(
    r"@pytest\.mark\.dependency\("
    r'name=["\'](?P<name>.+?)["\']'
    r"(?:,\s*depends=\[(?P<depends>[^\]]*)\])?"
)


def scan_test_file(file_path: str | Path) -> dict[str, list[dict]]:
    """掃描單一測試檔，回傳 group 結構。

    Usage:
        groups = scan_test_file("tests/test_maindesk_guest_function.py")
        # => {
        #   "test_maindesk_flow_c": [
        #     {"test_name": "test_add_note_at_maindesk", "depends": None},
        #     {"test_name": "test_add_guest_at_maindesk", "depends": "test_add_note_at_maindesk"},
        #     ...
        #   ],
        #   "_standalone": [...]
        # }
    """
    path = Path(file_path)
    if not path.is_absolute():
        path = _TESTS_DIR / path.name if path.name.startswith("test_") else _TESTS_DIR / file_path
    text = path.read_text(encoding="utf-8")

    groups: dict[str, list[dict]] = {}
    current_group = None
    current_dep_name = None
    current_depends = None

    for line in text.splitlines():
        line_stripped = line.strip()

        m_group = _GROUP_RE.search(line_stripped)
        if m_group:
            current_group = m_group.group(1)
            continue

        m_dep = _DEP_RE.search(line_stripped)
        if m_dep:
            current_dep_name = m_dep.group("name")
            raw_depends = m_dep.group("depends")
            if raw_depends:
                current_depends = [
                    d.strip().strip("'\"") for d in raw_depends.split(",") if d.strip()
                ]
            else:
                current_depends = None
            continue

        if line_stripped.startswith("def test_"):
            method_name = line_stripped.split("(")[0].replace("def ", "")
            entry = {
                "test_name": current_dep_name or method_name,
                "depends": current_depends,
            }
            group_key = current_group or "_standalone"
            groups.setdefault(group_key, []).append(entry)
            current_group = None
            current_dep_name = None
            current_depends = None

    return groups


def get_group_chain(file_path: str | Path, group_name: str) -> list[str]:
    """取得指定檔案中某 group 的 test_name chain（依宣告順序）。

    Usage:
        chain = get_group_chain("tests/test_maindesk_guest_function.py", "test_maindesk_flow_c")
        # => ["test_add_note_at_maindesk", "test_add_guest_at_maindesk", ...]
    """
    groups = scan_test_file(file_path)
    return [t["test_name"] for t in groups.get(group_name, [])]


def get_chain_tail(file_path: str | Path, group_name: str) -> list[str]:
    """取得 group 的葉節點（沒有被其他案例依賴的 test_name）。

    新案例的 depends 填這些。回傳空 list 代表 group 不存在或無案例。

    Usage:
        # 線性 chain → 單一葉節點
        get_chain_tail("test_maindesk_guest_function.py", "test_maindesk_flow_c")
        # => ["test_add_guest_todo_item_at_maindesk"]

        # 分支 → 多個葉節點
        get_chain_tail("test_room_control.py", "room_repair_visit")
        # => ["test_room_control_visit_floor", "test_room_control_modify_repair_visit",
        #     "test_room_control_clean_repair_rooms"]

        # 全獨立（無任何 depends）→ 所有案例都是葉節點
        get_chain_tail("test_xxx.py", "new_group")
        # => ["test_a", "test_b", "test_c"]
    """
    groups = scan_test_file(file_path)
    tests = groups.get(group_name, [])
    if not tests:
        return []

    depended_on = set()
    for t in tests:
        if t["depends"]:
            depended_on.update(t["depends"])

    leaves = [t["test_name"] for t in tests if t["test_name"] not in depended_on]
    return leaves


def validate_group(file_path: str | Path, group_name: str) -> list[str]:
    """檢查指定 group 是否違反 rules。從 .py decorator 掃描實際案例數。"""
    data = _load_data()
    rules = data.get("rules", {})
    warnings = []

    max_tests = rules.get("group_max_tests", 5)
    chain = get_group_chain(file_path, group_name)
    if len(chain) > max_tests:
        warnings.append(f"group '{group_name}' 有 {len(chain)} 個案例，超過上限 {max_tests}")

    return warnings


def validate_pages(file_path: str | Path) -> list[str]:
    """檢查 test 檔案中 pages 列表與 web.xxx 呼叫的一致性。

    雙向檢查：
    - web.xxx 用到但 class 不在 pages → 缺漏
    - pages 有但 web.xxx 沒用到 → 多餘

    Usage:
        warnings = validate_pages("tests/test_check_in_list.py")
        # => ["缺漏: web.base_page → BasePage 不在 pages 列表中",
        #     "多餘: pages 列表中 SharePanelComponent 未被 web.xxx 使用"]
        # 空 list = 全部 OK
    """
    path = Path(file_path)
    if not path.is_absolute():
        path = _TESTS_DIR / path.name if path.name.startswith("test_") else _TESTS_DIR / file_path
    text = path.read_text(encoding="utf-8")

    web_refs = set(re.findall(r"web\.(\w+)\.", text))

    pages_match = re.search(r"pages\s*=\s*\[([^\]]+)\]", text)
    if not pages_match:
        return ["pages = [...] 未找到"]
    page_classes = set(re.findall(r"(\w+)", pages_match.group(1)))

    def snake_to_pascal(name):
        return "".join(word.capitalize() for word in name.split("_"))

    used_classes = {snake_to_pascal(ref) for ref in web_refs}

    warnings = []
    for ref in sorted(web_refs):
        class_name = snake_to_pascal(ref)
        if class_name not in page_classes:
            warnings.append(f"缺漏: web.{ref} → {class_name} 不在 pages 列表中")
    for cls in sorted(page_classes):
        if cls not in used_classes:
            warnings.append(f"多餘: pages 列表中 {cls} 未被 web.xxx 使用")
    return warnings


def validate_resource(group_name: str, resource_key: str, value: str, env: str = None) -> list[str]:
    """檢查某資源是否已被其他 group 佔用。回傳警告訊息列表，空列表代表可用。

    Usage:
        warnings = validate_resource("test_maindesk_flow_c", "spare_part", "熨斗")
        # => ["spare_part '熨斗' 已被 test_maindesk_flow_b 使用"]
    """
    data = _load_data()
    if env is None:
        env = os.getenv("ENV", "autotest")
    groups = data["environments"][env]["groups"]
    warnings = []

    for gname, gdata in groups.items():
        if gname == group_name:
            continue
        common = gdata.get("common", {})
        if common.get(resource_key) == value:
            warnings.append(f"{resource_key} '{value}' 已被 {gname} 的 common 使用")
        for test_item in gdata.get("tests", []):
            if test_item.get(resource_key) == value:
                warnings.append(f"{resource_key} '{value}' 已被 {gname}.{test_item['key']} 使用")

    return warnings
