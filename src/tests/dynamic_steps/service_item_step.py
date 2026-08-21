from tests.dynamic_steps.base_steps.base_service_item_step import BaseServiceItemStep


class FirstDayServiceItemStep(BaseServiceItemStep):

    def clear_service_item(self):
        if self.web.reservation_card_dialog.get_tab_empty_msg("service") != "無任何資料":
            self.web.reservation_card_dialog.click_tab_toolbar("service", "刪除")

    def input_service_item_info(self, item, money, price_editable=True):
        self.web.service_item_component.click_service_dropdown("服務方式")
        self.web.service_item_component.select_dropdown_list("第一天").sleep(1)
        self.web.service_item_component.click_service_dropdown("服務項目")
        self.web.service_item_component.select_dropdown_list(item).sleep(1)

        if price_editable:
            self.web.service_item_component.input_service_column("單價", money)
        else:
            self.is_price_editable = self.web.service_item_component.unitprice_disable()

    def valid_tab_service_info(self, item, money, price_editable=True):
        self.web.base_page.assert_data(
            "服務類別",
            self.web.reservation_card_dialog.get_tab_service_info("commandOption"),
            "****: ALL",
        )
        self.web.base_page.assert_data(
            "服務項目", self.web.reservation_card_dialog.get_tab_service_info("itemNos"), item
        )
        self.web.base_page.assert_data(
            "數量規則",
            self.web.reservation_card_dialog.get_tab_service_info("itemQntRule"),
            "BY_USER: 自行輸入",
        )
        self.web.base_page.assert_data(
            "數量", self.web.reservation_card_dialog.get_tab_service_info("itemQuantity"), "1"
        )
        self.web.base_page.assert_data(
            "服務方式",
            self.web.reservation_card_dialog.get_tab_service_info("servWay"),
            "F: 第一天",
        )
        self.web.base_page.assert_data(
            "開始日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("beginDate"), ""
        )
        self.web.base_page.assert_data(
            "結束日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("endDate"), ""
        )
        self.web.base_page.assert_data(
            "來源",
            self.web.reservation_card_dialog.get_tab_service_info("fromSys"),
            "USER: 自行輸入",
        )

        if not price_editable:
            self.web.base_page.assert_data("價格不可編輯", self.is_price_editable, "true")
        else:
            self.web.base_page.assert_data(
                "單價", self.web.reservation_card_dialog.get_tab_service_info("unitAmount"), money
            )

    def valid_tab_expense_detail_info(self, item, money):
        # 檢查資料明細正確
        date = "2024/01/05"
        self.web.base_page.assert_data(
            "入帳日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "useDate"),
            "2024/01/05 週五",
        )
        self.web.base_page.assert_data(
            "消費項目",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemSna"),
            item,
        )
        self.web.base_page.assert_data(
            "單價",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "unitAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "數量",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemQnt"),
            "1",
        )
        self.web.base_page.assert_data(
            "小計",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "服務日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "servDate"),
            "2024/01/05 週五",
        )

        # 檢查每日費用是否包含服務項目
        self.web.base_page.assert_data(
            "1/5有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
            True,
        )
        self.web.base_page.assert_data(
            "1/6沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
            False,
        )
        self.web.base_page.assert_data(
            "1/7沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
            False,
        )
        self.web.base_page.assert_data(
            "1/8沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/08"),
            False,
        )
        self.web.base_page.assert_data(
            "1/9沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/09"),
            False,
        )
        self.web.base_page.assert_data(
            "1/10沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/10"),
            False,
        )


class DailyServiceItemStep(BaseServiceItemStep):

    def clear_service_item(self):
        if self.web.reservation_card_dialog.get_tab_empty_msg("service") != "無任何資料":
            self.web.reservation_card_dialog.click_tab_toolbar("service", "刪除")

    def input_service_item_info(self, item, money, price_editable=True):
        self.web.service_item_component.click_service_dropdown("服務方式")
        self.web.service_item_component.select_dropdown_list("每天").sleep(1)
        self.web.service_item_component.click_service_dropdown("服務項目")
        self.web.service_item_component.select_dropdown_list(item).sleep(1)

        if price_editable:
            self.web.service_item_component.input_service_column("單價", money)
        else:
            self.is_price_editable = self.web.service_item_component.unitprice_disable()

    def valid_tab_service_info(self, item, money, price_editable=True):
        self.web.base_page.assert_data(
            "服務類別",
            self.web.reservation_card_dialog.get_tab_service_info("commandOption"),
            "****: ALL",
        )
        self.web.base_page.assert_data(
            "服務項目", self.web.reservation_card_dialog.get_tab_service_info("itemNos"), item
        )
        self.web.base_page.assert_data(
            "數量規則",
            self.web.reservation_card_dialog.get_tab_service_info("itemQntRule"),
            "BY_USER: 自行輸入",
        )
        self.web.base_page.assert_data(
            "數量", self.web.reservation_card_dialog.get_tab_service_info("itemQuantity"), "1"
        )
        self.web.base_page.assert_data(
            "服務方式", self.web.reservation_card_dialog.get_tab_service_info("servWay"), "D: 每天"
        )
        self.web.base_page.assert_data(
            "開始日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("beginDate"), ""
        )
        self.web.base_page.assert_data(
            "結束日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("endDate"), ""
        )
        self.web.base_page.assert_data(
            "來源",
            self.web.reservation_card_dialog.get_tab_service_info("fromSys"),
            "USER: 自行輸入",
        )

        if not price_editable:
            self.web.base_page.assert_data("價格不可編輯", self.is_price_editable, "true")
        else:
            self.web.base_page.assert_data(
                "單價", self.web.reservation_card_dialog.get_tab_service_info("unitAmount"), money
            )

    def valid_tab_expense_detail_info(self, item, money):
        date = "2024/01/05"
        self.web.base_page.assert_data(
            "入帳日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "useDate"),
            "2024/01/05 週五",
        )
        self.web.base_page.assert_data(
            "消費項目",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemSna"),
            item,
        )
        self.web.base_page.assert_data(
            "單價",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "unitAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "數量",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemQnt"),
            "1",
        )
        self.web.base_page.assert_data(
            "小計",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "服務日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "servDate"),
            "2024/01/05 週五",
        )

        self.web.base_page.assert_data(
            "1/5有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
            True,
        )
        self.web.base_page.assert_data(
            "1/6有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
            True,
        )
        self.web.base_page.assert_data(
            "1/7有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
            True,
        )
        self.web.base_page.assert_data(
            "1/8有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/08"),
            True,
        )
        self.web.base_page.assert_data(
            "1/9有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/09"),
            True,
        )
        self.web.base_page.assert_data(
            "1/10有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/10"),
            True,
        )


class LastDayServiceItemStep(BaseServiceItemStep):

    def clear_service_item(self):
        if self.web.reservation_card_dialog.get_tab_empty_msg("service") != "無任何資料":
            self.web.reservation_card_dialog.click_tab_toolbar("service", "刪除")

    def input_service_item_info(self, item, money, price_editable=True):
        self.web.service_item_component.click_service_dropdown("服務方式")
        self.web.service_item_component.select_dropdown_list("最後一天").sleep(1)
        self.web.service_item_component.click_service_dropdown("服務項目")
        self.web.service_item_component.select_dropdown_list(item).sleep(1)

        if price_editable:
            self.web.service_item_component.input_service_column("單價", money)
        else:
            self.is_price_editable = self.web.service_item_component.unitprice_disable()

    def valid_tab_service_info(self, item, money, price_editable=True):
        self.web.base_page.assert_data(
            "服務類別",
            self.web.reservation_card_dialog.get_tab_service_info("commandOption"),
            "****: ALL",
        )
        self.web.base_page.assert_data(
            "服務項目", self.web.reservation_card_dialog.get_tab_service_info("itemNos"), item
        )
        self.web.base_page.assert_data(
            "數量規則",
            self.web.reservation_card_dialog.get_tab_service_info("itemQntRule"),
            "BY_USER: 自行輸入",
        )
        self.web.base_page.assert_data(
            "數量", self.web.reservation_card_dialog.get_tab_service_info("itemQuantity"), "1"
        )
        self.web.base_page.assert_data(
            "服務方式",
            self.web.reservation_card_dialog.get_tab_service_info("servWay"),
            "L: 最後一天",
        )
        self.web.base_page.assert_data(
            "開始日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("beginDate"), ""
        )
        self.web.base_page.assert_data(
            "結束日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("endDate"), ""
        )
        self.web.base_page.assert_data(
            "來源",
            self.web.reservation_card_dialog.get_tab_service_info("fromSys"),
            "USER: 自行輸入",
        )

        if not price_editable:
            self.web.base_page.assert_data("價格不可編輯", self.is_price_editable, "true")
        else:
            self.web.base_page.assert_data(
                "單價", self.web.reservation_card_dialog.get_tab_service_info("unitAmount"), money
            )

    def valid_tab_expense_detail_info(self, item, money):
        date = "2024/01/10"
        self.web.base_page.assert_data(
            "入帳日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "useDate"),
            "2024/01/10 週三",
        )
        self.web.base_page.assert_data(
            "消費項目",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemSna"),
            item,
        )
        self.web.base_page.assert_data(
            "單價",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "unitAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "數量",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemQnt"),
            "1",
        )
        self.web.base_page.assert_data(
            "小計",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "服務日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "servDate"),
            "2024/01/10 週三",
        )

        self.web.base_page.assert_data(
            "1/5沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
            False,
        )
        self.web.base_page.assert_data(
            "1/6沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
            False,
        )
        self.web.base_page.assert_data(
            "1/7沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
            False,
        )
        self.web.base_page.assert_data(
            "1/8沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/08"),
            False,
        )
        self.web.base_page.assert_data(
            "1/9沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/09"),
            False,
        )
        self.web.base_page.assert_data(
            "1/10有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/10"),
            True,
        )


class EveryFewDaysServiceItemStep(BaseServiceItemStep):

    def clear_service_item(self):
        if self.web.reservation_card_dialog.get_tab_empty_msg("service") != "無任何資料":
            self.web.reservation_card_dialog.click_tab_toolbar("service", "刪除")

    def input_service_item_info(self, item, money, price_editable=True):
        self.web.service_item_component.click_service_dropdown("服務方式")
        self.web.service_item_component.select_dropdown_list("每幾天").sleep(1)
        self.web.service_item_component.input_days_setting(2).sleep(1)
        self.web.service_item_component.click_confirm_days_setting().sleep(1)
        self.web.service_item_component.select_dropdown_list("每幾天").sleep(1)
        self.web.service_item_component.click_service_dropdown("服務項目")
        self.web.service_item_component.select_dropdown_list(item).sleep(1)

        if price_editable:
            self.web.service_item_component.input_service_column("單價", money)
        else:
            self.is_price_editable = self.web.service_item_component.unitprice_disable()

    def valid_tab_service_info(self, item, money, price_editable=True):
        self.web.base_page.assert_data(
            "服務類別",
            self.web.reservation_card_dialog.get_tab_service_info("commandOption"),
            "E2: 每2天",
        )
        self.web.base_page.assert_data(
            "服務項目", self.web.reservation_card_dialog.get_tab_service_info("itemNos"), item
        )
        self.web.base_page.assert_data(
            "數量規則",
            self.web.reservation_card_dialog.get_tab_service_info("itemQntRule"),
            "BY_USER: 自行輸入",
        )
        self.web.base_page.assert_data(
            "數量", self.web.reservation_card_dialog.get_tab_service_info("itemQuantity"), "1"
        )
        self.web.base_page.assert_data(
            "服務方式",
            self.web.reservation_card_dialog.get_tab_service_info("servWay"),
            "E: 每幾天",
        )
        self.web.base_page.assert_data(
            "開始日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("beginDate"), ""
        )
        self.web.base_page.assert_data(
            "結束日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("endDate"), ""
        )
        self.web.base_page.assert_data(
            "來源",
            self.web.reservation_card_dialog.get_tab_service_info("fromSys"),
            "USER: 自行輸入",
        )

        if not price_editable:
            self.web.base_page.assert_data("價格不可編輯", self.is_price_editable, "true")
        else:
            self.web.base_page.assert_data(
                "單價", self.web.reservation_card_dialog.get_tab_service_info("unitAmount"), money
            )

    def valid_tab_expense_detail_info(self, item, money):
        # 檢查資料明細正確
        date = "2024/01/06"
        self.web.base_page.assert_data(
            "入帳日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "useDate"),
            "2024/01/06 週六",
        )
        self.web.base_page.assert_data(
            "消費項目",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemSna"),
            item,
        )
        self.web.base_page.assert_data(
            "單價",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "unitAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "數量",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemQnt"),
            "1",
        )
        self.web.base_page.assert_data(
            "小計",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "服務日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "servDate"),
            "2024/01/06 週六",
        )

        # 檢查每日費用是否包含服務項目
        self.web.base_page.assert_data(
            "1/5沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
            False,
        )
        self.web.base_page.assert_data(
            "1/6有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
            True,
        )
        self.web.base_page.assert_data(
            "1/7沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
            False,
        )
        self.web.base_page.assert_data(
            "1/8有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/08"),
            True,
        )
        self.web.base_page.assert_data(
            "1/9沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/09"),
            False,
        )
        self.web.base_page.assert_data(
            "1/10有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/10"),
            True,
        )


class OnePlusEveryFewDaysServiceItemStep(BaseServiceItemStep):

    def clear_service_item(self):
        if self.web.reservation_card_dialog.get_tab_empty_msg("service") != "無任何資料":
            self.web.reservation_card_dialog.click_tab_toolbar("service", "刪除")

    def input_service_item_info(self, item, money, price_editable=True):
        self.web.service_item_component.click_service_dropdown("服務方式")
        self.web.service_item_component.select_dropdown_list("每1+N天").sleep(1)
        self.web.service_item_component.input_days_setting(2).sleep(1)
        self.web.service_item_component.click_confirm_days_setting().sleep(1)
        self.web.service_item_component.select_dropdown_list("每1+N天").sleep(1)
        self.web.service_item_component.click_service_dropdown("服務項目")
        self.web.service_item_component.select_dropdown_list(item).sleep(1)

        if price_editable:
            self.web.service_item_component.input_service_column("單價", money)
        else:
            self.is_price_editable = self.web.service_item_component.unitprice_disable()

    def valid_tab_service_info(self, item, money, price_editable=True):
        self.web.base_page.assert_data(
            "服務類別",
            self.web.reservation_card_dialog.get_tab_service_info("commandOption"),
            "N2: 每1+2天",
        )
        self.web.base_page.assert_data(
            "服務項目", self.web.reservation_card_dialog.get_tab_service_info("itemNos"), item
        )
        self.web.base_page.assert_data(
            "數量規則",
            self.web.reservation_card_dialog.get_tab_service_info("itemQntRule"),
            "BY_USER: 自行輸入",
        )
        self.web.base_page.assert_data(
            "數量", self.web.reservation_card_dialog.get_tab_service_info("itemQuantity"), "1"
        )
        self.web.base_page.assert_data(
            "服務方式",
            self.web.reservation_card_dialog.get_tab_service_info("servWay"),
            "N: 每1+N天",
        )
        self.web.base_page.assert_data(
            "開始日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("beginDate"), ""
        )
        self.web.base_page.assert_data(
            "結束日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("endDate"), ""
        )
        self.web.base_page.assert_data(
            "來源",
            self.web.reservation_card_dialog.get_tab_service_info("fromSys"),
            "USER: 自行輸入",
        )

        if not price_editable:
            self.web.base_page.assert_data("價格不可編輯", self.is_price_editable, "true")
        else:
            self.web.base_page.assert_data(
                "單價", self.web.reservation_card_dialog.get_tab_service_info("unitAmount"), money
            )

    def valid_tab_expense_detail_info(self, item, money):
        # 檢查資料明細正確
        date = "2024/01/05"
        self.web.base_page.assert_data(
            "入帳日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "useDate"),
            "2024/01/05 週五",
        )
        self.web.base_page.assert_data(
            "消費項目",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemSna"),
            item,
        )
        self.web.base_page.assert_data(
            "單價",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "unitAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "數量",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemQnt"),
            "1",
        )
        self.web.base_page.assert_data(
            "小計",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "服務日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "servDate"),
            "2024/01/05 週五",
        )

        # 檢查每日費用是否包含服務項目
        self.web.base_page.assert_data(
            "1/5有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
            True,
        )
        self.web.base_page.assert_data(
            "1/6沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
            False,
        )
        self.web.base_page.assert_data(
            "1/7有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
            True,
        )
        self.web.base_page.assert_data(
            "1/8沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/08"),
            False,
        )
        self.web.base_page.assert_data(
            "1/9有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/09"),
            True,
        )
        self.web.base_page.assert_data(
            "1/10沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/10"),
            False,
        )


class WeeklyServiceItemStep(BaseServiceItemStep):

    def clear_service_item(self):
        if self.web.reservation_card_dialog.get_tab_empty_msg("service") != "無任何資料":
            self.web.reservation_card_dialog.click_tab_toolbar("service", "刪除")

    def input_service_item_info(self, item, money, price_editable=True):
        self.web.service_item_component.click_service_dropdown("服務方式")
        self.web.service_item_component.select_dropdown_list("每周").sleep(1)
        self.web.service_item_component.click_weekday_dropdown_column().sleep(1)
        self.web.service_item_component.select_weekday_dropdown_list("周一")
        self.web.service_item_component.select_weekday_dropdown_list("周二")
        self.web.service_item_component.click_weekday_dropdown_column()
        self.web.service_item_component.click_confirm_days_setting()
        self.web.service_item_component.select_dropdown_list("每周").sleep(1)
        self.web.service_item_component.click_service_dropdown("服務項目")
        self.web.service_item_component.select_dropdown_list(item).sleep(1)

        if price_editable:
            self.web.service_item_component.input_service_column("單價", money)
        else:
            self.is_price_editable = self.web.service_item_component.unitprice_disable()

    def valid_tab_service_info(self, item, money, price_editable=True):
        self.web.base_page.assert_data(
            "服務類別",
            self.web.reservation_card_dialog.get_tab_service_info("commandOption"),
            "W2,W3: 周一,周二",
        )
        self.web.base_page.assert_data(
            "服務項目", self.web.reservation_card_dialog.get_tab_service_info("itemNos"), item
        )
        self.web.base_page.assert_data(
            "數量規則",
            self.web.reservation_card_dialog.get_tab_service_info("itemQntRule"),
            "BY_USER: 自行輸入",
        )
        self.web.base_page.assert_data(
            "數量", self.web.reservation_card_dialog.get_tab_service_info("itemQuantity"), "1"
        )
        self.web.base_page.assert_data(
            "服務方式", self.web.reservation_card_dialog.get_tab_service_info("servWay"), "W: 每周"
        )
        self.web.base_page.assert_data(
            "開始日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("beginDate"), ""
        )
        self.web.base_page.assert_data(
            "結束日期(空值)", self.web.reservation_card_dialog.get_tab_service_info("endDate"), ""
        )
        self.web.base_page.assert_data(
            "來源",
            self.web.reservation_card_dialog.get_tab_service_info("fromSys"),
            "USER: 自行輸入",
        )

        if not price_editable:
            self.web.base_page.assert_data("價格不可編輯", self.is_price_editable, "true")
        else:
            self.web.base_page.assert_data(
                "單價", self.web.reservation_card_dialog.get_tab_service_info("unitAmount"), money
            )

    def valid_tab_expense_detail_info(self, item, money):
        date = "2024/01/08"
        self.web.base_page.assert_data(
            "入帳日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "useDate"),
            "2024/01/08 週一",
        )
        self.web.base_page.assert_data(
            "消費項目",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemSna"),
            item,
        )
        self.web.base_page.assert_data(
            "單價",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "unitAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "數量",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemQnt"),
            "1",
        )
        self.web.base_page.assert_data(
            "小計",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "服務日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "servDate"),
            "2024/01/08 週一",
        )

        self.web.base_page.assert_data(
            "1/5沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
            False,
        )
        self.web.base_page.assert_data(
            "1/6沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
            False,
        )
        self.web.base_page.assert_data(
            "1/7沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
            False,
        )
        self.web.base_page.assert_data(
            "1/8有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/08"),
            True,
        )
        self.web.base_page.assert_data(
            "1/9有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/09"),
            True,
        )
        self.web.base_page.assert_data(
            "1/10沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/10"),
            False,
        )


class SpecifiedDateServiceItemStep(BaseServiceItemStep):

    def clear_service_item(self):
        if self.web.reservation_card_dialog.get_tab_empty_msg("service") != "無任何資料":
            self.web.reservation_card_dialog.click_tab_toolbar("service", "刪除")

    def input_service_item_info(self, item, money, price_editable=True):
        self.web.service_item_component.click_service_dropdown("服務方式")
        self.web.service_item_component.select_dropdown_list("指定日期").sleep(1)
        self.web.service_item_component.click_input_column("開始日期")
        self.web.service_item_component.click_start_date("6")
        self.web.service_item_component.click_input_column("結束日期")
        self.web.service_item_component.click_end_date("8")
        self.web.service_item_component.click_service_dropdown("服務項目")
        self.web.service_item_component.select_dropdown_list(item).sleep(1)

        if price_editable:
            self.web.service_item_component.input_service_column("單價", money)
        else:
            self.is_price_editable = self.web.service_item_component.unitprice_disable()

    def valid_tab_service_info(self, item, money, price_editable=True):
        self.web.base_page.assert_data(
            "服務類別",
            self.web.reservation_card_dialog.get_tab_service_info("commandOption"),
            "****: ALL",
        )
        self.web.base_page.assert_data(
            "服務項目", self.web.reservation_card_dialog.get_tab_service_info("itemNos"), item
        )
        self.web.base_page.assert_data(
            "數量規則",
            self.web.reservation_card_dialog.get_tab_service_info("itemQntRule"),
            "BY_USER: 自行輸入",
        )
        self.web.base_page.assert_data(
            "數量", self.web.reservation_card_dialog.get_tab_service_info("itemQuantity"), "1"
        )
        self.web.base_page.assert_data(
            "服務方式",
            self.web.reservation_card_dialog.get_tab_service_info("servWay"),
            "A: 指定日期",
        )
        self.web.base_page.assert_data(
            "開始日期",
            self.web.reservation_card_dialog.get_tab_service_info("beginDate"),
            "2024/01/06 週六",
        )
        self.web.base_page.assert_data(
            "結束日期",
            self.web.reservation_card_dialog.get_tab_service_info("endDate"),
            "2024/01/08 週一",
        )
        self.web.base_page.assert_data(
            "來源",
            self.web.reservation_card_dialog.get_tab_service_info("fromSys"),
            "USER: 自行輸入",
        )

        if not price_editable:
            self.web.base_page.assert_data("價格不可編輯", self.is_price_editable, "true")
        else:
            self.web.base_page.assert_data(
                "單價", self.web.reservation_card_dialog.get_tab_service_info("unitAmount"), money
            )

    def valid_tab_expense_detail_info(self, item, money):
        date = "2024/01/06"
        self.web.base_page.assert_data(
            "入帳日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "useDate"),
            "2024/01/06 週六",
        )
        self.web.base_page.assert_data(
            "消費項目",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemSna"),
            item,
        )
        self.web.base_page.assert_data(
            "單價",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "unitAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "數量",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemQnt"),
            "1",
        )
        self.web.base_page.assert_data(
            "小計",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "itemAmount"),
            money,
        )
        self.web.base_page.assert_data(
            "服務日",
            self.web.reservation_card_dialog.get_tab_expense_info_in_row(date, "servDate"),
            "2024/01/06 週六",
        )

        self.web.base_page.assert_data(
            "1/5沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
            False,
        )
        self.web.base_page.assert_data(
            "1/6有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
            True,
        )
        self.web.base_page.assert_data(
            "1/7有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
            True,
        )
        self.web.base_page.assert_data(
            "1/8有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/08"),
            True,
        )
        self.web.base_page.assert_data(
            "1/9沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/09"),
            False,
        )
        self.web.base_page.assert_data(
            "1/10沒有費用",
            item in self.web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/10"),
            False,
        )
