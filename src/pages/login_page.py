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
MAX_LOGIN_RETRIES = 10
# 重試之間的退避秒數：auth 服務限流是懲罰視窗制——每次提交（不分
# 對錯）都會重置視窗，視窗內一律回「驗證碼錯誤」（答案正確也一樣）。
# 實測安靜 5 分鐘後單發即成功、60 秒退避連發全滅；退避必須長於視窗
RETRY_BACKOFF_SECONDS = 300
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
            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )

        retry = 0
        attempts = []
        self.input(self.locator.input_username, username)

        if AppConfig.is_sso_login():
            outcome = None
            while retry < MAX_LOGIN_RETRIES:
                if retry > 0:
                    # 前一次提交成功、頁面正在轉跳（此環境轉跳可達 30 秒）
                    if "auth.athena.com.tw" not in self.driver.current_url:
                        break
                    # 先退避再重試：密集提交會被一律拒絕（見 RETRY_BACKOFF_SECONDS）
                    sleep(RETRY_BACKOFF_SECONDS)
                    # 失敗後 Keycloak 重渲染的表單不保證保留密碼欄
                    # （帳號被暴力防護盯上後甚至直接移除）；重新導向
                    # 乾淨的 auth URL 重填全部欄位最穩健
                    self.driver.get(DriverHelper.build_auth_url())
                    sleep(1)
                    self.input(self.locator.input_username, username)
                self.input(self.locator.input_password, password)
                self.captcha_screenshot()
                captcha_text, conf, solver = self._solve_captcha(captcha_model)
                self._record_captcha_attempt(
                    attempts, retry + 1, captcha_text, conf, solver
                )
                self.input_with_clear(
                    self.locator.input_valid_code, captcha_text.strip()
                )
                self.click(self.locator.btn_login)
                retry += 1
                # 提交後等待明確結果：跳轉（成功）或錯誤提示（重試）。
                # 只查一次提示會在提示未渲染時誤判成「完成」而提前出場；
                # 轉跳（token 交換）有時超過 8 秒，等待要夠長。
                outcome = self._wait_submit_outcome()
                if outcome == "redirect":
                    break
        else:
            self.input(self.locator.input_password, password)
            while retry == 0 or (retry < MAX_LOGIN_RETRIES and self.has_dialog_tip()):
                self.close_dialog_tip()
                self.captcha_screenshot()
                captcha_text, conf, solver = self._solve_captcha(captcha_model)
                self._record_captcha_attempt(
                    attempts, retry + 1, captcha_text, conf, solver
                )
                self.input_with_clear(
                    self.locator.input_valid_code, captcha_text.strip()
                )
                self.click(self.locator.btn_login)
                retry += 1

        login_ok = self._wait_login_redirect()
        self._mark_last_captcha_outcome(attempts, login_ok)
        print(
            f"[captcha] login {'OK' if login_ok else 'FAIL'}: {len(attempts)} attempts"
        )

        sleep(1)
        DriverHelper.save_session_storages()
        return self

    def _solve_captcha(self, captcha_model):
        """ML 模型優先，無模型時用 pytesseract OCR；回傳 (文字, 信心度, 解法)"""
        if captcha_model is not None:
            try:
                text, conf = captcha_model.predict_captcha_detailed(
                    str(CAPTCHA_IMAGE_PATH)
                )
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
            dest = (
                CAPTCHA_SAMPLES_DIR / f"{ts}_a{number}_{text}_c{conf:.2f}_{solver}.png"
            )
            shutil.copy(CAPTCHA_IMAGE_PATH, dest)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"[captcha] sample save failed: {e}")

    def _wait_submit_outcome(self, timeout=20):
        """提交後輪詢至明確結果：回傳 redirect（成功跳轉）/ wrong_captcha（重試）/ timeout"""
        polled = 0.0
        while polled < timeout:
            if "auth.athena.com.tw" not in self.driver.current_url:
                return "redirect"
            if self.has_wrong_captcha_tip():
                return "wrong_captcha"
            sleep(0.25)
            polled += 0.25
        return "timeout"

    def _wait_login_redirect(self, timeout=5):
        """最後一次提交後的轉跳是非同步的：等 URL 離開 auth 再判定成敗，
        否則會把已成功的登入誤判為失敗（並錯標樣本）"""
        sleep_seconds = 0.25
        waited = 0.0
        while waited < timeout:
            if "auth.athena.com.tw" not in self.driver.current_url:
                return True
            sleep(sleep_seconds)
            waited += sleep_seconds
        return False

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
        # 直接拍「畫面上這張」驗證碼，不點擊刷新：失敗重試都是整頁
        # 重新導向（見 login()），頁面上的碼本來就是新的；點擊刷新會
        # 觸發非同步換圖，截圖與提交之間碼可能再換一次，導致「讀對
        # 舊圖、提交時答案已換新」的隱性失敗（伺服器回驗證碼錯誤）
        captcha_element = self.driver.find_element(*self.locator.img_captcha)
        # 等圖片解碼完成才截圖，避免拍到半空白圖
        for _ in range(20):
            if self.driver.execute_script(
                "var a=arguments[0]; return a.complete && a.naturalWidth>0;",
                captcha_element,
            ):
                break
            sleep(0.25)
        sleep(0.3)
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
