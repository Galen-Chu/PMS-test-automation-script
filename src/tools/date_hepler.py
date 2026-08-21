class DateHelper:

    @staticmethod
    def month_number_to_name(month_number):
        months = {
            "01": "一月",
            "02": "二月",
            "03": "三月",
            "04": "四月",
            "05": "五月",
            "06": "六月",
            "07": "七月",
            "08": "八月",
            "09": "九月",
            "10": "十月",
            "11": "十一月",
            "12": "十二月",
        }
        return months.get(month_number, None)

    @staticmethod
    def clear_0_prefix(value):
        if isinstance(value, str):
            return value.lstrip("0")
        return value
