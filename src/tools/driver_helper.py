import json
import os
from pathlib import Path
import urllib
from time import sleep
import humps
from selenium.common.exceptions import UnexpectedAlertPresentException


class Browser:
    """以共用 driver 建立的 page-object 組合（取代動態 type('Expando') 屬性袋）

    屬性名稱維持 decamelize(類別名稱)，測試端使用方式不變（web.maindesk_page、
    web.driver 等），但有了明確型別、可讀的 repr 與 IDE 支援。
    """

    def __init__(self, driver, pages):
        self.driver = driver
        for page in pages:
            setattr(self, humps.decamelize(page.__name__), page(driver))

    def page_names(self):
        return sorted(name for name in vars(self) if name != "driver")

    def __repr__(self):
        return f"Browser(pages={', '.join(self.page_names())})"


class DriverHelper:

    DRIVER = None
    TMP_SESSION = Path(__file__).resolve().parent / "session_storages.json"

    @staticmethod
    def get_logged_in_browser(pages, path=None):
        """使用已登入的共用 driver 建立頁面物件（搭配 logged_in_driver fixture）

        Args:
            pages: Page Object class 清單
            path: 頁面路徑。None=停留當前頁；"login"=前往登入頁；其他=前往指定頁面
        """
        web_driver = DriverHelper.DRIVER
        if web_driver is None:
            raise RuntimeError("DriverHelper.DRIVER is None — 請先使用 logged_in_driver fixture")

        if path == "login":
            web_driver.get(DriverHelper.build_auth_url())
        elif path:
            from selenium.webdriver.support.ui import WebDriverWait

            target = f"{os.getenv('WEB_URL')}/pms/{os.getenv('ENV_NUM')}/{path}"
            web_driver.get(target)

            def booted(d):
                """PMS SPA 完成啟動＝body 有實質內容。

                啟動期間可能短暫拋出 JS alert（boot 錯誤訊息，關掉後 App
                會繼續完成載入）；在等待條件內順手掃掉，避免阻斷後續操作。"""
                try:
                    text = d.execute_script(
                        "return (document.body && document.body.innerText || '').trim()"
                    )
                    return len(text) > 30
                except UnexpectedAlertPresentException:
                    try:
                        d.switch_to.alert.accept()
                    except Exception:
                        pass
                    return False

            WebDriverWait(web_driver, 20).until(booted)

        return Browser(web_driver, pages)

    @staticmethod
    def save_session_storages():
        session_data_dict = DriverHelper.DRIVER.execute_script("""
            let data = {};
            for (let [key, value] of Object.entries(sessionStorage)) {
                data[key] = value;
            }
            return data;
        """)
        with open(DriverHelper.TMP_SESSION, "w", encoding="utf-8") as file:
            json.dump(session_data_dict, file)

    @staticmethod
    def build_auth_url():
        base_url = os.getenv("BASE_URL")
        redirect_url = os.getenv("REDIRECT_URL")
        client_id = os.getenv("CLIENT_ID", "internal")
        language = os.getenv("LANGUAGE")

        params = {
            "response_type": "code",
            "client_id": client_id,
            "scope": "openid offline_access",
            "redirect_uri": redirect_url,
            "ui_locales": language,
        }
        return f"{base_url}?{urllib.parse.urlencode(params)}"
