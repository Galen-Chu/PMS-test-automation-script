from tests.dynamic_steps.base_steps.base_valid_column_step import BaseValidColumnStep


class IdOnlyRateCodColumnStep(BaseValidColumnStep):

    def input_data(self):
        self.web.share_panel_component.input_by_label_3("房價代號", "Normal")
        self.web.share_panel_component.input_by_label_3("房價名稱", "errortest")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價").sleep(2)

    def assert_result(self):
        self.web.rate_cod_dialog.click_data_field_id("save").sleep(2)
        self.web.base_page.assert_data_in_list(
            "房價代號Normal已存在，無法重複新增",
            self.web.tip_component.get_tip_text(),
            "房價代號Normal已存在，無法重複新增",
        )


class DaysOverMaxRateCodColumnStep(BaseValidColumnStep):

    def input_data(self):
        self.web.share_panel_component.input_by_label_3("最少住宿天數", "1000")

    def assert_result(self):
        self.web.rate_cod_dialog.click_data_field_id("save").sleep(2)
        self.web.base_page.assert_data(
            "最少住宿天數需於0~999之間",
            self.web.tip_component.get_tip_text(),
            "最少住宿天數需於0~999之間",
        )


class ServiceOverMaxRateCodColumnStep(BaseValidColumnStep):

    def input_data(self):
        self.web.share_panel_component.input_by_label_3("服務費%", "1000")

    def assert_result(self):
        self.web.rate_cod_dialog.click_data_field_id("save").sleep(2)
        self.web.base_page.assert_data(
            "服務費需於0~100之間", self.web.tip_component.get_tip_text(), "服務費需於0~100之間"
        )


class ComOverMaxRateCodColumnStep(BaseValidColumnStep):

    def input_data(self):
        self.web.share_panel_component.input_by_label_3("佣金%", "1000")

    def assert_result(self):
        self.web.rate_cod_dialog.click_data_field_id("save").sleep(2)
        self.web.base_page.assert_data(
            "佣金需於0~100之間", self.web.tip_component.get_tip_text(), "佣金需於0~100之間"
        )


class DpRatOverMaxRateCodColumnStep(BaseValidColumnStep):

    def input_data(self):
        self.web.share_panel_component.input_by_label_3("房價代號", "errortest")
        self.web.share_panel_component.input_by_label_3("房價名稱", "errortest")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "DR:浮動房價")
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "DP:價格連動").sleep(
            1
        )
        self.web.share_panel_component.select_by_label_span_3("連動主房價", "Dynamic").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("價格調整規則", "RAT:%").sleep(1)
        self.web.share_panel_component.input_by_label_3("調整數字", "1000")

    def assert_result(self):
        self.web.base_page.assert_data(
            "最大值為 100", self.web.share_panel_component.get_value_by_label_3("調整數字"), "100"
        )


class DpAmtOverMaxRateCodColumnStep(BaseValidColumnStep):

    def input_data(self):
        self.web.share_panel_component.input_by_label_3("房價代號", "errortest")
        self.web.share_panel_component.input_by_label_3("房價名稱", "errortest")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "DR:浮動房價")
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "DP:價格連動").sleep(
            1
        )
        self.web.share_panel_component.select_by_label_span_3("連動主房價", "Dynamic").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("價格調整規則", "AMT:$").sleep(1)
        self.web.share_panel_component.input_by_label_3("調整數字", "1000000")

    def assert_result(self):
        self.web.base_page.assert_data(
            "最大值為 99,999",
            self.web.share_panel_component.get_value_by_label_3("調整數字"),
            "99999",
        )
