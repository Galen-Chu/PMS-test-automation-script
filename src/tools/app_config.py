import os


class AppConfig:
    """PMS 環境設定的單一存取點（VERSION 等環境變數的解析與驗證）"""

    @staticmethod
    def version():
        raw = os.getenv("VERSION")
        if raw is None or not raw.strip().isdigit():
            raise RuntimeError(
                "環境變數 VERSION 未正確設定（應為整數，例如 131）；"
                "請於 pytest.ini 或環境變數提供，參考 pytest.ini.example"
            )
        return int(raw)

    @classmethod
    def is_sso_login(cls):
        """VERSION >= 130 走 SSO auth 登入頁，否則為舊版 PMS 登入頁"""
        return cls.version() >= 130
