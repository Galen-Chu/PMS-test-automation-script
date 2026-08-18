import json
import os
from pathlib import Path
import urllib
from time import sleep
import humps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service


class DriverHelper:

    DRIVER = None
    TMP_SESSION = Path(__file__).resolve().parent / "session_storages.json"

    @staticmethod
    def create_web_browser(pages, sys="sso", path="login"):
        options = ChromeOptions()

        options.add_argument("--start-maximized")
        options.add_argument("--guest")
        options.add_experimental_option(
            "prefs",
            {
                "profile.default_content_setting_values": {"notifications": 2},
            },
        )

        selenium_hub = os.getenv("SELENIUM_HUB")

        if selenium_hub:
            web_driver = webdriver.Remote(command_executor=selenium_hub, options=options)
            sleep(5)
        else:
            web_driver = webdriver.Chrome(service=Service(), options=options)

        web_driver.implicitly_wait(10)
        web_driver.delete_all_cookies()

        if path == "login" and int(os.getenv("VERSION")) >= 130:
            login_url = DriverHelper.build_auth_url()
            web_driver.get(login_url)
        else:
            web_driver.get(f"{os.getenv('WEB_URL')}")
            sleep(2)

            if sys != "sso":
                # 從文件中讀取 sessionStorage 數據
                with open(DriverHelper.TMP_SESSION, "r", encoding="utf-8") as file:
                    session_data_dict = json.load(file)
                # 還原數據到 sessionStorage
                for key, value in session_data_dict.items():
                    web_driver.execute_script(f"sessionStorage.setItem('{key}', '{value}');")
            web_driver.get(f"{os.getenv('WEB_URL')}/{sys}/{os.getenv('ENV_NUM')}/{path}")

        tmp_pages = {}
        for page in pages:
            tmp_pages[humps.decamelize(page.__name__)] = page(web_driver)
        web = type("Expando", (object,), tmp_pages)()
        web.driver = web_driver
        DriverHelper.DRIVER = web_driver
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
