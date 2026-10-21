import os
from time import sleep
from PIL import Image
import pytesseract
from tools.driver_helper import DriverHelper
from pages.base_page import BasePage


class LoginPage(BasePage):

    def login(self, username, password):
        # Lazy import: keeps the TF/cv2 stack out of module import time, so
        # collecting unrelated tests does not require the ML dependencies.
        captcha_model = None
        try:
            from tools.captcha.captcha_helper import CaptchaTrainer

            captcha_model = CaptchaTrainer()
            captcha_model.load_model()
        except Exception:
            # ML 模型未訓練或相依套件未安裝，改用 pytesseract OCR
            captcha_model = None

        # 設定 tesseract 路徑（Windows 安裝位置）
        import shutil

        if not shutil.which("tesseract"):
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        retry = 0
        self.input(self.locator.input_username, username)

        if int(os.getenv("VERSION")) >= 130:
            while retry == 0 or (retry < 30 and self.has_wrong_captcha_tip()):
                # 若已離開 auth 頁面（登入成功跳轉），跳出迴圈
                if retry > 0 and "auth.athena.com.tw" not in self.driver.current_url:
                    break
                self.input(self.locator.input_password, password)
                self.captcha_screenshot()
                captcha_text = self._solve_captcha(captcha_model)
                self.input_with_clear(self.locator.input_valid_code, captcha_text.strip())
                self.click(self.locator.btn_login)
                retry += 1
        else:
            self.input(self.locator.input_password, password)
            while retry == 0 or (retry < 30 and self.has_dialog_tip()):
                self.close_dialog_tip()
                self.captcha_screenshot()
                captcha_text = self._solve_captcha(captcha_model)
                self.input_with_clear(self.locator.input_valid_code, captcha_text.strip())
                self.click(self.locator.btn_login)
                retry += 1

        sleep(1)
        DriverHelper.save_session_storages()
        return self

    def _solve_captcha(self, captcha_model):
        """ML 模型優先，無模型時用 pytesseract OCR"""
        if captcha_model is not None:
            try:
                return captcha_model.predict_captcha("image.png")
            except Exception:
                pass
        # pytesseract 後備
        image = Image.open("image.png")
        processed_image = image.convert("L").resize((400, 128))
        captcha_text = pytesseract.image_to_string(
            processed_image,
            config="-l eng -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 13",
        )
        return captcha_text

    def captcha_screenshot(self, fix=""):
        captcha_element = self.driver.find_element(*self.locator.img_captcha)
        captcha_element.click()
        sleep(2)
        captcha_element.screenshot(f"image{fix}.png")
        return self

    def has_dialog_tip(self):
        return self.has_element(self.locator.dialog_tip)

    def close_dialog_tip(self):
        if self.has_dialog_tip():
            self.click(self.locator.dialog_tip_btn)
        return self

    def has_wrong_captcha_tip(self):
        return self.has_element(self.locator.wrong_captcha_tip)
