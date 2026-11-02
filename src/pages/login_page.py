import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from time import sleep
from PIL import Image
import pytesseract
from tools.app_config import AppConfig
from tools.driver_helper import DriverHelper
from pages.athena_base_page import AthenaBasePage
from locators.login_locator import LoginLocator

# 驗證碼截圖寫到系統暫存（不污染工作目錄）
CAPTCHA_IMAGE_PATH = Path(tempfile.gettempdir()) / "pms_captcha.png"
# 登入（含驗證碼辨識失敗重試）���最大嘗試次數
MAX_LOGIN_RETRIES = 30
# 驗證碼樣本收集目錄（gitignored；檔名帶預測與信心度，
# 成功登入的最後一次會加 _OK 後綴 = 自帶正確標籤的訓練樣本）
CAPTCHA_SAMPLES_DIR = Path("captcha_data/attempts")


class LoginPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, LoginLocator())

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
        if not shutil.which("tesseract"):
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        retry = 0
        attempts = []
        self.input(self.locator.input_username, username)

        if AppConfig.is_sso_login():
            while retry == 0 or (retry < MAX_LOGIN_RETRIES and self.has_wrong_captcha_tip()):
                # 若已離開 auth 頁面（登入成功跳轉），跳出迴圈
                if retry > 0 and "auth.athena.com.tw" not in self.driver.current_url:
                    break
                self.input(self.locator.input_password, password)
                self.captcha_screenshot()
                captcha_text, conf, solver = self._solve_captcha(captcha_model)
                self._record_captcha_attempt(attempts, retry + 1, captcha_text, conf, solver)
                self.input_with_clear(self.locator.input_valid_code, captcha_text.strip())
                self.click(self.locator.btn_login)
                retry += 1
        else:
            self.input(self.locator.input_password, password)
            while retry == 0 or (retry < MAX_LOGIN_RETRIES and self.has_dialog_tip()):
                self.close_dialog_tip()
                self.captcha_screenshot()
                captcha_text, conf, solver = self._solve_captcha(captcha_model)
                self._record_captcha_attempt(attempts, retry + 1, captcha_text, conf, solver)
                self.input_with_clear(self.locator.input_valid_code, captcha_text.strip())
                self.click(self.locator.btn_login)
                retry += 1

        login_ok = "auth.athena.com.tw" not in self.driver.current_url
        self._mark_last_captcha_outcome(attempts, login_ok)
        print(f"[captcha] login {'OK' if login_ok else 'FAIL'}: {len(attempts)} attempts")

        sleep(1)
        DriverHelper.save_session_storages()
        return self

    def _solve_captcha(self, captcha_model):
        """ML 模型優先，無模型時用 pytesseract OCR；回傳 (文字, 信心度, 解法)"""
        if captcha_model is not None:
            try:
                text, conf = captcha_model.predict_captcha_detailed(str(CAPTCHA_IMAGE_PATH))
                return text, conf, "ml"
            except Exception:
                pass
        # pytesseract 後備（無信心度概念，設 0）
        image = Image.open(CAPTCHA_IMAGE_PATH)
        processed_image = image.convert("L").resize((400, 128))
        captcha_text = pytesseract.image_to_string(
            processed_image,
            config="-l eng -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 13",
        )
        return captcha_text, 0.0, "ocr"

    def _record_captcha_attempt(self, attempts, number, text, conf, solver):
        """記錄並保存每次驗證碼嘗試（供準確率分析與訓練資料收集）"""
        attempts.append({"n": number, "text": text, "conf": conf, "solver": solver})
        print(f"[captcha] attempt {number}: {text} (conf={conf:.2f}, {solver})")
        try:
            CAPTCHA_SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            dest = CAPTCHA_SAMPLES_DIR / f"{ts}_a{number}_{text}_c{conf:.2f}_{solver}.png"
            shutil.copy(CAPTCHA_IMAGE_PATH, dest)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"[captcha] sample save failed: {e}")

    def _mark_last_captcha_outcome(self, attempts, login_ok):
        """成功登入時，最後一次嘗試的樣本即為正確標籤（檔名加 _OK）"""
        if not attempts:
            return
        last = attempts[-1]
        try:
            for f in CAPTCHA_SAMPLES_DIR.glob(f"*_a{last['n']}_{last['text']}_*"):
                suffix = "_OK" if login_ok else "_FAIL"
                f.rename(f.with_name(f.stem + suffix + f.suffix))
        except Exception:  # pylint: disable=broad-exception-caught
            pass

    def captcha_screenshot(self):
        captcha_element = self.driver.find_element(*self.locator.img_captcha)
        captcha_element.click()
        sleep(2)  # 等驗證碼圖片刷新（無 DOM 條件可等待）
        captcha_element.screenshot(str(CAPTCHA_IMAGE_PATH))
        return self

    def has_dialog_tip(self):
        return self.has_element(self.locator.dialog_tip)

    def close_dialog_tip(self):
        if self.has_dialog_tip():
            self.click(self.locator.dialog_tip_btn)
        return self

    def has_wrong_captcha_tip(self):
        return self.has_element(self.locator.wrong_captcha_tip)
