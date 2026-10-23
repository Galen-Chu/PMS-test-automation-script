# -*- coding: utf-8 -*-
"""A3 驗收：ML 驗證碼模型登入效率測試

本腳本不內建任何真實帳密或網址；請以環境變數提供設定後執行：
    python src/tools/verify_a3_login.py   (需先 export/set USERNAME/PASSWORD 等)
"""

import os, sys, time

os.environ.setdefault("VERSION", "133")
os.environ.setdefault("WEB_URL", "https://demo.example.com")
os.environ.setdefault(
    "BASE_URL", "https://auth.example.com/protocol/openid-connect/auth"
)
os.environ.setdefault("REDIRECT_URL", "https://demo.example.com/callback")
os.environ.setdefault("CLIENT_ID", "internal")
os.environ.setdefault("LANGUAGE", "zh-TW")
os.environ.setdefault("ENV_NUM", "1")

for _required in ("USERNAME", "PASSWORD"):
    if not os.environ.get(_required):
        sys.exit(f"[!] 請先設定 {_required} 環境變數（本腳本不內建帳密）")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.driver_helper import DriverHelper
from pages.login_page import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service

print("=" * 60)
print("A3 驗收：ML 驗證碼模型 vs pytesseract OCR 效率比較")
print("=" * 60)

# Step 0: 確認 ML 模型可用
print("\n[0] 檢查 ML 模型...")
try:
    from tools.captcha.captcha_helper import CaptchaTrainer

    trainer = CaptchaTrainer()
    trainer.load_model()
    print("    ML 模型載入成功 ✓")
    print(f"    字元集: {trainer.mappings['characters']}")
    ml_available = True
except Exception as e:
    print(f"    ML 模型載入失敗: {e}")
    print("    將使用 pytesseract OCR 後備")
    ml_available = False

# Step 1: 開瀏覽器
print("\n[1] 啟動 Chrome...")
opts = ChromeOptions()
opts.add_argument("--start-maximized")
opts.add_argument("--guest")
driver = webdriver.Chrome(service=Service(), options=opts)
driver.implicitly_wait(10)
DriverHelper.DRIVER = driver

# Step 2: 導航到登入頁
print("\n[2] 導航到登入頁...")
driver.get(DriverHelper.build_auth_url())
time.sleep(3)
print(f"    URL: {driver.current_url[:60]}")

# Step 3: 計時登入
print(f"\n[3] 開始登入（{'ML 模型' if ml_available else 'pytesseract OCR'}）...")
t0 = time.time()

login_page = LoginPage(driver)
login_page.login(os.environ["USERNAME"], os.environ["PASSWORD"])

elapsed = time.time() - t0
print(f"\n    登入完成！")
print(f"    耗時: {elapsed:.1f} 秒")
print(f"    最終 URL: {driver.current_url[:60]}")

# Step 4: 驗證登入成功
body = driver.find_element("tag name", "body").text
if "請重新登入" in body:
    print("    [X] 登入失敗（重新登入提示）")
else:
    print("    [OK] 登入成功 ✓")

# 比較
print("\n" + "=" * 60)
print("效率比較")
print("=" * 60)
print(f"  pytesseract OCR 基準: ~120 秒（昨天測試）")
print(f"  ML 模型本次:          {elapsed:.1f} 秒")
print(f"  改善:                 {120/elapsed:.1f}x" if elapsed > 0 else "")

driver.quit()
print("\n驗收完成！")
