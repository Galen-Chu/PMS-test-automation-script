import json
import os
from pathlib import Path
import urllib
import humps


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
            web_driver.get(f"{os.getenv('WEB_URL')}/pms/{os.getenv('ENV_NUM')}/{path}")

        tmp_pages = {}
        for page in pages:
            tmp_pages[humps.decamelize(page.__name__)] = page(web_driver)
        web = type("Expando", (object,), tmp_pages)()
        web.driver = web_driver
        return web

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
