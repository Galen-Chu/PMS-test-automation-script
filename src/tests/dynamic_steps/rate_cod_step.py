from time import sleep
import allure
from tests.dynamic_steps.base_steps.base_rate_cod_step import BaseRateCodStep


# 預設已填好欄位，需要才調整
class CMPRateCodStep(BaseRateCodStep):

    # 使用說明、CMP 計價方式
    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.input_by_label_3("使用說明", "免費招待，VIP客戶、公關。")
        self.web.share_panel_component.select_by_label_span_3("計價方式", "CMP:COMPLIMENTARY")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "02:旅行社訂房").sleep(1)

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [4000, 4000]).sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [3000, 3000]).sleep(1)
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [400, 400]).sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [300, 300]).sleep(1)
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [200, 200]).sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [150, 150]).sleep(1)

    def set_service_items(self):
        pass

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "CMP:COMPLIMENTARY",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "02:旅行社訂房",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class DRRateCodStep(BaseRateCodStep):

    # ID 不連動 、 DR 計價方式
    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "DR:浮動房價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "02:旅行社訂房").sleep(1)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "DR:浮動房價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "02:旅行社訂房",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class DURateCodStep(BaseRateCodStep):

    # DU 計價方式

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "DU:Day use")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "DU:Day use",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "DU:DAY USE",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class GRRateCodStep(BaseRateCodStep):

    # GR 計價方式
    # 多語系

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", "以天計價")
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)
        self.web.rate_cod_dialog.click_localization_ratecod().sleep(1)
        self.web.rate_cod_dialog.input_name_by_lang("繁體中文", "以天計價")
        self.web.rate_cod_dialog.input_name_by_lang("English", "GR")
        self.web.rate_cod_dialog.input_name_by_lang("日本語", "単位での価格")
        self.web.rate_cod_dialog.input_name_by_lang("Tiếng Việt", "Giá tính")
        self.web.rate_cod_dialog.click_lang_confirm()

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [5000, 5000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [4000, 4000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [500, 500])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [400, 400])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [250, 250])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [200, 200])

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), "以天計價"
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class HURateCodStep(BaseRateCodStep):

    # HU 計價方式

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "HU:HOUSE USE")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "HU:HOUSE USE",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class MBRateCodStep(BaseRateCodStep):

    # MON 計價方式 + 月初入帳

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "MON:以月計價")
        self.web.share_panel_component.select_by_label_span_3(
            "入帳方式", "BEGIN_OF_MONTH:月初入帳"
        ).sleep(1)
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "MON:以月計價",
        )
        web.base_page.assert_data(
            "入帳方式",
            web.share_panel_component.get_value_by_label_span_3("入帳方式"),
            "BEGIN_OF_MONTH:月初入帳",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )

        web.rate_cod_dialog.click_tab("serviceItem").sleep(1)
        web.rate_cod_dialog.click_grid_add().sleep(1)
        web.rate_cod_dialog.click_charge_type()
        web.rate_cod_dialog.screenshot("服務項目-月初入帳無法使用內含服務")
        sleep(2)
        tmp_list = web.rate_cod_dialog.get_service_types()
        web.rate_cod_dialog.assert_data_in_list(
            "服務項目-月初入帳只能選擇外加服務", tmp_list, "Q:N"
        )
        web.rate_cod_dialog.assert_data_not_in_list(
            "服務項目-月初入帳無法使用內含服務", tmp_list, "I:Y"
        )


class MDRateCodStep(BaseRateCodStep):

    # MON 計價方式 + 逐日入帳

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "MON:以月計價")
        self.web.share_panel_component.select_by_label_span_3("入帳方式", "DAILY:逐日入帳").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "MON:以月計價",
        )
        web.base_page.assert_data(
            "入帳方式",
            web.share_panel_component.get_value_by_label_span_3("入帳方式"),
            "DAILY:逐日入帳",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )

        web.rate_cod_dialog.click_tab("serviceItem").sleep(1)
        web.rate_cod_dialog.click_grid_add().sleep(1)
        web.rate_cod_dialog.click_charge_type()
        web.rate_cod_dialog.screenshot("服務項目-月初入帳無法使用內含服務")
        sleep(2)
        tmp_list = web.rate_cod_dialog.get_service_types()
        web.rate_cod_dialog.assert_data_in_list(
            "服務項目-月初入帳可以選擇外加服務", tmp_list, "Q:N"
        )
        web.rate_cod_dialog.assert_data_in_list(
            "服務項目-月初入帳可以選擇內含服務", tmp_list, "I:Y"
        )


class MERateCodStep(BaseRateCodStep):

    # MON 計價方式 + 月底入帳

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "MON:以月計價")
        self.web.share_panel_component.select_by_label_span_3(
            "入帳方式", "END_OF_MONTH:月底入帳"
        ).sleep(1)
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "MON:以月計價",
        )
        web.base_page.assert_data(
            "入帳方式",
            web.share_panel_component.get_value_by_label_span_3("入帳方式"),
            "END_OF_MONTH:月底入帳",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )

        web.rate_cod_dialog.click_tab("serviceItem").sleep(1)
        web.rate_cod_dialog.click_grid_add().sleep(1)
        web.rate_cod_dialog.click_charge_type()
        web.rate_cod_dialog.screenshot("服務項目-月初入帳無法使用內含服務")
        sleep(2)
        tmp_list = web.rate_cod_dialog.get_service_types()
        web.rate_cod_dialog.assert_data_in_list(
            "服務項目-月初入帳可以選擇外加服務", tmp_list, "Q:N"
        )
        web.rate_cod_dialog.assert_data_not_in_list(
            "服務項目-月初入帳無法使用內含服務", tmp_list, "I:Y"
        )


class NSTRateCodStep(BaseRateCodStep):

    # NST 計價方式

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "NST:不統計")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "NST:不統計",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class RTRateCodStep(BaseRateCodStep):

    # RT 計價方式

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "RT:以時計價")
        self.web.share_panel_component.select_by_label_span_3("住宿時數", "3").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "RT:以時計價",
        )
        web.base_page.assert_data(
            "住宿時間", web.share_panel_component.get_value_by_label_span_3("住宿時數"), "3"
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源", web.share_panel_component.get_value_by_label_span_3("訂房來源"), "RT:休息"
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )
        web.share_panel_component.assert_data(
            "服務項目不顯示", web.share_panel_component.has_toolbar_item("服務項目"), False
        )


class SaleRateCodStep(BaseRateCodStep):

    # 銷售期間
    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)
        self.web.rate_cod_dialog.input_sale_duration(["2024年/1月/9", "2024年/12月/30"])

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [5000, 5000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [4000, 4000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [500, 500])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [400, 400])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [250, 250])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [200, 200])

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class ConRateCodStep(BaseRateCodStep):

    # 合約價

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.click_label_checkbox("合約價")
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "C:合約公司價")
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動")
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [2000, 2000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [1000, 1000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [200, 200])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [100, 100])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [100, 100])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [50, 50])

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "C:合約公司價",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class AddRateCodStep(BaseRateCodStep):

    # 加收房價

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.click_label_checkbox("是否加收")
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用")
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動")
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [2000, 2000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [1000, 1000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [200, 200])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [100, 100])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [100, 100])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [50, 50])

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class ComRateCodStep(BaseRateCodStep):

    # 有佣金 可異動
    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.click_label_checkbox("佣金異動")
        self.web.share_panel_component.input_by_label_3("佣金%", "10")
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用")
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動")
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [2000, 2000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [1000, 1000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [200, 200])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [100, 100])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [100, 100])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [50, 50])

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class FixRateCodStep(BaseRateCodStep):

    # 房價異動
    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.click_label_checkbox("房價異動")
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用")
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動")
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶")

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [2000, 2000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [1000, 1000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [200, 200])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [100, 100])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [100, 100])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [50, 50])

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class DaysRateCodStep(BaseRateCodStep):

    # 最少住宿
    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用")
        self.web.share_panel_component.input_by_label_3("最少住宿天數", "2")
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動")
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶")

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [2000, 2000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [1000, 1000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [200, 200])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [100, 100])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [100, 100])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [50, 50])

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class RateRateCodStep(BaseRateCodStep):

    # 人數加價規則 ： 依房價人數
    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("人數加價規則", "RATE_COD:依房價人數")
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "ID:不連動")
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶")

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [2000, 2000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [1000, 1000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [200, 200])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [100, 100])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [100, 100])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [50, 50])
        self.web.rate_cod_dialog.click_tab("stander").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("stander", "標準人數", [2, 2])

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.rate_cod_dialog.click_tab("stander")
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "RATE_COD:依房價人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "ID:不連動",
        )


class BSRateCodStep(BaseRateCodStep):

    def input_rate_cod_info(self, rate_cod):
        DPRatRateCodStep.set_base_rate_cod(rate_cod[:8])
        DPAmtRateCodStep.set_base_rate_cod(rate_cod[:8])
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "BS:主要房價").sleep(
            1
        )
        self.web.share_panel_component.select_by_label_span_3("訂房來源", "01:簽約客戶").sleep(1)

    def set_use_duration(self):
        self.web.rate_cod_dialog.click_add_use_date().sleep(1)
        self.web.rate_cod_dialog.add_new_use_date().sleep(1)
        self.web.rate_cod_dialog.click_date_icon("beginDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "1月", "7")
        self.web.rate_cod_dialog.click_date_icon("endDate").sleep(1)
        self.web.rate_cod_dialog.select_date("2024年", "12月", "30")
        self.web.rate_cod_dialog.click_data_field_id("commandOption").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["HH:假日", "HN:平日"])
        self.web.rate_cod_dialog.click_data_field_id("roomCodes").sleep(1)
        self.web.rate_cod_dialog.select_multiple_item(["STD:標準客房", "SDT:雅緻客房"]).sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("confirmButton").sleep(1)

    def set_rate_cod_price(self):
        self.web.rate_cod_dialog.click_tab("roomRent").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [2000, 2000])
        self.web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [1000, 1000])
        self.web.rate_cod_dialog.click_tab("addAdult").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [200, 200])
        self.web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [100, 100])
        self.web.rate_cod_dialog.click_tab("addChild").sleep(1)
        self.web.rate_cod_dialog.input_values_by_row("addChild", "假日", [100, 100])
        self.web.rate_cod_dialog.input_values_by_row("addChild", "平日", [50, 50])

    def set_service_items(self):
        self.web.rate_cod_dialog.click_tab("serviceItem").sleep(1)
        self.web.rate_cod_dialog.add_service_item().sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("servWay").sleep(1)
        self.web.rate_cod_dialog.select_dropdown_list("D:每天")
        self.web.rate_cod_dialog.click_data_field_id("itemNos").sleep(1)
        self.web.rate_cod_dialog.select_dropdown_list("2008:早餐")
        sleep(2)
        self.web.rate_cod_dialog.click_data_field_id_down("commandOption").sleep(1)
        self.web.rate_cod_dialog.click_dropdown_all()
        self.web.rate_cod_dialog.select_dropdown_list("H:假日")
        self.web.rate_cod_dialog.select_dropdown_list("N:平日")
        self.web.rate_cod_dialog.click_data_field_id("itemQntRule").sleep(1)
        self.web.rate_cod_dialog.select_dropdown_list("BY_ADULT:大人人數")

        self.web.rate_cod_dialog.add_service_item().sleep(1)
        self.web.rate_cod_dialog.add_service_item().sleep(1)
        self.web.rate_cod_dialog.click_data_field_id("servWay").sleep(1)
        self.web.rate_cod_dialog.select_dropdown_list("F:第一天")
        sleep(2)
        self.web.rate_cod_dialog.click_data_field_id_down("commandOption").sleep(1)
        self.web.rate_cod_dialog.click_dropdown_all()
        self.web.rate_cod_dialog.select_dropdown_list("H:假日")
        self.web.rate_cod_dialog.select_dropdown_list("N:平日")
        self.web.rate_cod_dialog.click_data_field_id("chargeType").sleep(1)
        self.web.rate_cod_dialog.select_dropdown_list("Q:N")
        self.web.rate_cod_dialog.click_data_field_id("itemQntRule").sleep(1)
        self.web.rate_cod_dialog.select_dropdown_list("BY_ADULT:大人人數")
        self.web.rate_cod_dialog.click_data_field_id("itemNos").sleep(1)
        self.web.rate_cod_dialog.select_dropdown_list("1006:SPA")
        sleep(2)
        self.web.base_page.screenshot("新增服務項目")
        self.web.rate_cod_dialog.click_data_field_id("save").sleep(2)
        self.web.tip_component.click_ok().sleep(2)

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.base_page.assert_data(
            "房價代號-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("房價代號"),
            False,
        )
        web.base_page.assert_data(
            "計價方式-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("計價方式"),
            False,
        )
        web.base_page.assert_data(
            "價格連動屬性-是否能填寫",
            web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
            True,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "01:簽約客戶",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "BS:主要房價",
        )


class DPRatRateCodStep(BaseRateCodStep):

    bs_rate_cod = ""

    @classmethod
    def set_base_rate_cod(cls, rate_cod):
        cls.bs_rate_cod = rate_cod

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "DP:價格連動").sleep(
            1
        )
        self.web.share_panel_component.select_by_label_span_3("連動主房價", self.bs_rate_cod)
        self.web.share_panel_component.select_by_label_span_3("價格調整規則", "RAT:%").sleep(1)
        self.web.share_panel_component.input_by_label_3("調整數字", "10")

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.share_panel_component.assert_data(
            "無法使用使用期間", web.rate_cod_dialog.item_enabled("+"), False
        )
        web.share_panel_component.assert_data(
            "無法調整人數加價規則",
            web.share_panel_component.get_is_enabled_by_label_3("人數加價規則"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "04:自行訂房",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "DP:價格連動",
        )
        web.base_page.assert_data(
            "連動主房價",
            web.share_panel_component.get_value_by_label_span_3("連動主房價"),
            self.bs_rate_cod,
        )
        web.base_page.assert_data(
            "價格調整規則",
            web.share_panel_component.get_value_by_label_span_3("價格調整規則"),
            "RAT:%",
        )
        web.base_page.assert_data(
            "調整數字", web.share_panel_component.get_value_by_label_3("調整數字"), "10"
        )

        web.rate_cod_dialog.click_tab("serviceItem").sleep(1)
        web.base_page.screenshot("服務項目唯獨無法新增、刪除、編輯")
        web.base_page.assert_data(
            "DP房價-服務項目唯獨無法新增、刪除、編輯", web.rate_cod_dialog.has_disable_grid(), True
        )

        with allure.step("驗證BS房價無法更改價格連動屬性"):
            web.rate_cod_dialog.close_panel()
            web.base_page.clear().sleep(2)
            web.base_page.set_value_by_label("房價代號", self.bs_rate_cod)
            web.base_page.search().sleep(2)
            web.base_page.click_target_rate_cod(self.bs_rate_cod).sleep(2)
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.screenshot("驗證BS房價無法更改價格連動屬性")
            web.base_page.assert_data(
                "價格連動屬性-是否能填寫",
                web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
                False,
            )


class DPAmtRateCodStep(BaseRateCodStep):

    bs_rate_cod = ""

    @classmethod
    def set_base_rate_cod(cls, rate_cod):
        cls.bs_rate_cod = rate_cod

    def input_rate_cod_info(self, rate_cod):
        self.web.share_panel_component.input_by_label_3("房價代號", rate_cod)
        self.web.share_panel_component.input_by_label_3("房價名稱", rate_cod)
        self.web.share_panel_component.select_by_label_span_3("計價方式", "GR:以天計價")
        self.web.share_panel_component.select_by_label_span_3("房價群組", "F:散客專用").sleep(1)
        self.web.share_panel_component.select_by_label_span_3("價格連動屬性", "DP:價格連動").sleep(
            1
        )
        self.web.share_panel_component.select_by_label_span_3("連動主房價", self.bs_rate_cod)
        self.web.share_panel_component.select_by_label_span_3("價格調整規則", "AMT:$").sleep(1)
        self.web.share_panel_component.input_by_label_3("調整數字", "100")

    def valid_rate_cod_info(self, rate_cod):
        web = self.web
        web.share_panel_component.assert_data(
            "無法使用使用期間", web.rate_cod_dialog.item_enabled("+"), False
        )
        web.share_panel_component.assert_data(
            "無法調整人數加價規則",
            web.share_panel_component.get_is_enabled_by_label_3("人數加價規則"),
            False,
        )
        web.base_page.assert_data(
            "合約價-是否能填寫",
            web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
            False,
        )
        web.base_page.assert_data(
            "房價代號", web.share_panel_component.get_value_by_label_3("房價代號"), rate_cod[:8]
        )
        web.base_page.assert_data(
            "房價名稱", web.share_panel_component.get_value_by_label_3("房價名稱"), rate_cod
        )
        web.base_page.assert_data(
            "計價方式",
            web.share_panel_component.get_value_by_label_span_3("計價方式"),
            "GR:以天計價",
        )
        web.base_page.assert_data(
            "房價群組",
            web.share_panel_component.get_value_by_label_span_3("房價群組"),
            "F:散客專用",
        )
        web.base_page.assert_data(
            "訂房來源",
            web.share_panel_component.get_value_by_label_span_3("訂房來源"),
            "04:自行訂房",
        )
        web.base_page.assert_data(
            "市場類別", web.share_panel_component.get_value_by_label_span_3("市場類別"), "FIT:散客"
        )
        web.base_page.assert_data(
            "人數加價規則",
            web.share_panel_component.get_value_by_label_span_3("人數加價規則"),
            "ROOM_COD:依房型人數",
        )
        web.base_page.assert_data(
            "價格連動屬性",
            web.share_panel_component.get_value_by_label_span_3("價格連動屬性"),
            "DP:價格連動",
        )
        web.base_page.assert_data(
            "連動主房價",
            web.share_panel_component.get_value_by_label_span_3("連動主房價"),
            self.bs_rate_cod,
        )
        web.base_page.assert_data(
            "價格調整規則",
            web.share_panel_component.get_value_by_label_span_3("價格調整規則"),
            "AMT:$",
        )
        web.base_page.assert_data(
            "調整數字", web.share_panel_component.get_value_by_label_3("調整數字"), "100"
        )

        web.rate_cod_dialog.click_tab("serviceItem").sleep(1)
        web.base_page.screenshot("服務項目唯獨無法新增、刪除、編輯")
        web.base_page.assert_data(
            "DP房價-服務項目唯獨無法新增、刪除、編輯", web.rate_cod_dialog.has_disable_grid(), True
        )

        with allure.step("驗證BS房價無法更改價格連動屬性"):
            web.rate_cod_dialog.close_panel()
            web.base_page.clear().sleep(2)
            web.base_page.set_value_by_label("房價代號", self.bs_rate_cod)
            web.base_page.search().sleep(2)
            web.base_page.click_target_rate_cod(self.bs_rate_cod).sleep(2)
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.screenshot("驗證BS房價無法更改價格連動屬性")
            web.base_page.assert_data(
                "價格連動屬性-是否能填寫",
                web.share_panel_component.get_is_enabled_by_label_3("價格連動屬性"),
                False,
            )
