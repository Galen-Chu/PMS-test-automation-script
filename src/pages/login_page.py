import os
from time import sleep
from PIL import Image
import pytesseract
from tools.captcha.captcha_helper import CaptchaTrainer
from tools.driver_helper import DriverHelper
from pages.base_page import BasePage


class LoginPage(BasePage):

    def login(self, username, password):
        captcha_model = CaptchaTrainer()
        captcha_model.load_model()
        retry = 0
        self.input(self.locator.input_username, username)

        if int(os.getenv("VERSION")) >= 130:
            while retry == 0 or (retry < 30 and self.has_wrong_captcha_tip()):
                self.input(self.locator.input_password, password)
                self.captcha_screenshot()
                captcha_text = captcha_model.predict_captcha("image.png")
                self.input_with_clear(self.locator.input_valid_code, captcha_text.strip())
                self.click(self.locator.btn_login)
                retry += 1
        else:
            self.input(self.locator.input_password, password)
            while retry == 0 or (retry < 30 and self.has_dialog_tip()):
                self.close_dialog_tip()
                self.captcha_screenshot()
                image = Image.open("image.png")
                processed_image = image.convert("L")
                captcha_text = pytesseract.image_to_string(
                    processed_image, config="-l eng -c tessedit_char_whitelist=0123456789 --psm 13"
                )
                self.input_with_clear(self.locator.input_valid_code, captcha_text.strip())
                self.click(self.locator.btn_login)
                retry += 1

        sleep(1)
        DriverHelper.save_session_storages()
        return self

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
