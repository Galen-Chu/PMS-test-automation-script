import os
from selenium.webdriver.common.by import By


class LoginLocator:

    input_password = (By.XPATH, "//input[@placeholder='密碼']")
    input_valid_code = (By.XPATH, "//input[@placeholder='驗證碼']")
    img_captcha = (By.XPATH, "//img[@id='captchaImg']")

    dialog_tip = (By.XPATH, "//div[@role='dialog' and @aria-label='提示']")
    dialog_tip_btn = (By.XPATH, "//div[@role='dialog' and @aria-label='提示']//button/span")

    # ----- 130與128登入頁切換 -----
    btn_login = (
        (By.XPATH, "//button[@id='kc-login']")
        if int(os.getenv("VERSION")) >= 130
        else (By.XPATH, "//a[@id='login_btn']")
    )
    input_username = (
        (By.XPATH, "//input[@placeholder='使用者名稱']")
        if int(os.getenv("VERSION")) >= 130
        else (By.XPATH, "//input[@placeholder='使用者']")
    )
    wrong_captcha_tip = (By.XPATH, "//span[text()='驗證碼錯誤']")
    # ----- 130與128登入頁切換 結束-----
