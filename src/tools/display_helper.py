import re


class DisplayHelper:

    @staticmethod
    def normalize_display_value(value):
        """combobox 編輯值 → grid 顯示格式（冒號兩側固定單空格）。

        編輯態 input value 無空格（'x:y'）、存檔後 grid 顯示有空格（'x : y'）；
        本來就有空格的值（hotel '01 : x'）恆等不變。
        """
        return re.sub(r"\s*:\s*", " : ", value)
