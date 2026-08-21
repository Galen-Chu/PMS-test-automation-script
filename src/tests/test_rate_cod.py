import allure
import pytest
from selenium.common.exceptions import NoSuchElementException
from pages.base_page import BasePage
from pages.components.company_panel_component import CompanyPanelComponent
from pages.components.header_component import HeaderComponent
from pages.components.service_item_component import ServiceItemComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.dialogs.rate_cod_dialog import RateCodDialog

# pylint: disable=unused-import
from tests.dynamic_steps.rate_cod_step import (
    CMPRateCodStep,
    DRRateCodStep,
    DURateCodStep,
    GRRateCodStep,
    HURateCodStep,
    MBRateCodStep,
    MDRateCodStep,
    MERateCodStep,
    NSTRateCodStep,
    RTRateCodStep,
    SaleRateCodStep,
    ConRateCodStep,
    AddRateCodStep,
    ComRateCodStep,
    FixRateCodStep,
    DaysRateCodStep,
    RateRateCodStep,
    BSRateCodStep,
    DPRatRateCodStep,
    DPAmtRateCodStep,
)
from tests.dynamic_steps.rate_cod_column_step import (
    IdOnlyRateCodColumnStep,
    DaysOverMaxRateCodColumnStep,
    ServiceOverMaxRateCodColumnStep,
    ComOverMaxRateCodColumnStep,
    DpRatOverMaxRateCodColumnStep,
    DpAmtOverMaxRateCodColumnStep,
)

# pylint: enable=unused-import
from tools.driver_helper import DriverHelper
from tools.random_helper import RandomHelper


@allure.feature("房價")
class TestRateCod:

    @allure.story("新增房價")
    @pytest.mark.parametrize(
        "rate_code_type",
        [
            "CMP",
            "DR",
            "DU",
            "GR",
            "HU",
            "MB",
            "MD",
            "ME",
            "RT",
            "Rate",
            "Sale",
            "Add",
            "Com",
            "Fix",
            "Days",
        ],
    )
    def test_create_new_rate_cod(self, rate_code_type):
        pages = [
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            ServiceItemComponent,
            RateCodDialog,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        rate_cod_step = globals()[f"{rate_code_type}RateCodStep"](web)

        with allure.step("開啟房價新增視窗"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.click_toolbar_with_icon("add").sleep(2)
            web.base_page.screenshot("開啟房價新增視窗")

        with allure.step("填入房價資訊並儲存成功"):
            rate_cod_name = f"{rate_code_type}{RandomHelper.random_string(3)}"
            rate_cod_step.input_rate_cod_info(rate_cod_name)
            rate_cod_step.set_use_duration()
            rate_cod_step.set_rate_cod_price()
            web.rate_cod_dialog.click_data_field_id("save").sleep(2)
            web.base_page.screenshot("填入房價資訊並儲存成功")
            web.tip_component.click_ok().sleep(2)
            rate_cod_step.set_service_items()
            web.rate_cod_dialog.close_panel()

        with allure.step("驗證新增房價資料"):
            web.base_page.set_value_by_label("房價代號", rate_cod_name[:8])
            web.base_page.search().sleep(2)
            web.base_page.click_target_rate_cod(rate_cod_name[:8])
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.screenshot("驗證新增房價資料")
            rate_cod_step.valid_rate_cod_info(rate_cod_name)

    @allure.story("新增連動屬性房價")
    @pytest.mark.xdist_group("bs_rate_cod")
    @pytest.mark.parametrize("rate_code_type", ["BS", "DPRat", "DPAmt"])
    def test_create_bs_rate_cod(self, rate_code_type):
        pages = [
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            ServiceItemComponent,
            RateCodDialog,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        rate_cod_step = globals()[f"{rate_code_type}RateCodStep"](web)

        with allure.step("開啟房價新增視窗"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.click_toolbar_with_icon("add").sleep(2)
            web.base_page.screenshot("開啟房價新增視窗")

        with allure.step("填入房價資訊並儲存成功"):
            rate_cod_name = f"{rate_code_type}{RandomHelper.random_string(3)}"
            rate_cod_step.input_rate_cod_info(rate_cod_name)
            rate_cod_step.set_use_duration()
            rate_cod_step.set_rate_cod_price()
            web.rate_cod_dialog.click_data_field_id("save").sleep(2)
            web.base_page.screenshot("填入房價資訊並儲存成功")
            web.tip_component.click_ok().sleep(2)
            rate_cod_step.set_service_items()
            web.rate_cod_dialog.close_panel()

        with allure.step("驗證新增房價資料"):
            web.base_page.set_value_by_label("房價代號", rate_cod_name[:8])
            web.base_page.search().sleep(2)
            web.base_page.click_target_rate_cod(rate_cod_name[:8])
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.screenshot("驗證新增房價資料")
            rate_cod_step.valid_rate_cod_info(rate_cod_name)

    @allure.story("新增房價-無法使用功能")
    def test_create_ratecod_not_use(self):
        pages = [HeaderComponent, TipComponent, SharePanelComponent, BasePage, RateCodDialog]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("開啟房價新增視窗"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.click_toolbar_with_icon("add").sleep(2)

        with allure.step("驗證功能按鈕無法使用"):
            web.base_page.screenshot("驗證功能按鈕無法使用")
            web.share_panel_component.assert_data(
                "無法使用浮動房價", web.rate_cod_dialog.item_enabled("浮動房價"), False
            )
            web.share_panel_component.assert_data(
                "無法使用上傳官網", web.rate_cod_dialog.item_enabled("上傳官網"), False
            )
            web.share_panel_component.assert_data(
                "無法使用複製房價", web.rate_cod_dialog.item_enabled("複製房價"), False
            )
            web.share_panel_component.assert_data(
                "無法使用期間一覽表", web.rate_cod_dialog.item_enabled("期間一覽表"), False
            )
            web.share_panel_component.assert_data(
                "無法使用房價試算", web.rate_cod_dialog.item_enabled("房價試算"), False
            )

    @allure.story("新增房價-輸入欄位驗證")
    @pytest.mark.parametrize(
        "valid_type",
        ["DaysOverMax", "ServiceOverMax", "ComOverMax", "DpRatOverMax", "DpAmtOverMax", "IdOnly"],
    )
    def test_rate_cod_columns_valid(self, valid_type):
        pages = [HeaderComponent, TipComponent, SharePanelComponent, BasePage, RateCodDialog]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        step = globals()[f"{valid_type}RateCodColumnStep"](web)

        with allure.step("開啟房價新增視窗"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.click_toolbar_with_icon("add").sleep(2)
            web.base_page.screenshot("開啟房價新增視窗")

        with allure.step("新增房價-輸入欄位驗證"):
            step.input_data()
            web.base_page.screenshot("新增房價-輸入欄位驗證")

        with allure.step("驗證提示訊息"):
            step.assert_result()
            web.base_page.screenshot("驗證提示訊息")

    @allure.story("搜尋房價-銷售中為必填")
    def test_search_rate_cod_required(self):
        pages = [HeaderComponent, TipComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("移除'銷售中'搜尋條件"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.select("銷售中", "Y : 是")
            web.base_page.screenshot("移除銷售中搜尋條件")

        with allure.step("搜尋房價-銷售中為必填"):
            web.base_page.search().sleep(2)
            web.base_page.assert_data(
                "銷售中 為必填", web.tip_component.get_tip_text(), "銷售中 為必填"
            )
            web.base_page.screenshot("搜尋房價-銷售中為必填")

    @allure.story("搜尋房價-查無資料-重新查詢")
    def test_search_rate_cod_not_found_retry(self):
        pages = [HeaderComponent, TipComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("搜尋房價-查無資料"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.set_value_by_label("房價代號", "查無資料")
            web.base_page.search().sleep(2)
            web.base_page.assert_data("無符合資料", web.tip_component.get_tip_text(), "無符合資料")
            web.base_page.screenshot("搜尋房價-查無資料")
            web.tip_component.click_ok().sleep(2)

        with allure.step("重新查詢房價-有資料"):
            web.base_page.clear().sleep(2)
            web.base_page.search().sleep(2)
            web.base_page.assert_data_has_count(
                "重新查詢房價-有資料", web.base_page.get_diplaying_items_count()
            )
            web.base_page.screenshot("重新查詢房價")

    @allure.story("編輯房價-有特殊約會顯示列表-開啟特殊約")
    def test_edit_rate_cod_special_contract(self):
        pages = [HeaderComponent, TipComponent, SharePanelComponent, BasePage, RateCodDialog]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("查詢房價列表"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.set_value_by_label("房價代號", "comcon2")
            web.base_page.search().sleep(2)
            web.base_page.screenshot("查詢房價列表")

        with allure.step("編輯房價-有特殊約會顯示列表"):
            web.base_page.click_target_rate_cod("comcon2")
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.rate_cod_dialog.click_tab("specialContract").sleep(1)
            web.rate_cod_dialog.screenshot("編輯房價-有特殊約會顯示列表")
            web.rate_cod_dialog.assert_data(
                "編輯房價-有特殊約會顯示列表", web.rate_cod_dialog.has_cratecod_mn("測測BB22"), True
            )
            web.rate_cod_dialog.assert_data(
                "房價名稱可以更改",
                web.share_panel_component.get_is_enabled_by_label_3("房價名稱"),
                True,
            )
            web.rate_cod_dialog.assert_data(
                "房價群組可以更改",
                web.share_panel_component.get_is_enabled_by_label_3("房價群組"),
                True,
            )
            web.rate_cod_dialog.assert_data(
                "使用說明可以更改",
                web.share_panel_component.get_is_enabled_by_label_3("使用說明"),
                True,
            )
            web.rate_cod_dialog.assert_data(
                "銷售中可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("銷售中"),
                True,
            )
            web.rate_cod_dialog.assert_data(
                "合約價可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "佣金異動可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("佣金異動"),
                True,
            )
            web.rate_cod_dialog.assert_data(
                "房價異動可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("房價異動"),
                True,
            )
            web.rate_cod_dialog.assert_data(
                "網訂使用可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("網訂使用"),
                True,
            )
            web.rate_cod_dialog.assert_data(
                "是否加收可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("是否加收"),
                True,
            )
            web.rate_cod_dialog.assert_data(
                "會員積點可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("會員積點"),
                True,
            )

        with allure.step("驗證特殊約欄位"):
            web.rate_cod_dialog.click_cratecod_mn("測測BB22").sleep(4)
            web.rate_cod_dialog.screenshot("驗證特殊約欄位")
            web.rate_cod_dialog.assert_data(
                "房價名稱可以更改",
                web.share_panel_component.get_is_enabled_by_label_3("房價名稱"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "房價群組可以更改",
                web.share_panel_component.get_is_enabled_by_label_3("房價群組"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "使用說明可以更改",
                web.share_panel_component.get_is_enabled_by_label_3("使用說明"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "銷售中可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("銷售中"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "合約價可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("合約價"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "佣金異動可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("佣金異動"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "房價異動可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("房價異動"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "網訂使用可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("網訂使用"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "是否加收可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("是否加收"),
                False,
            )
            web.rate_cod_dialog.assert_data(
                "會員積點可以更改",
                web.share_panel_component.get_is_enabled_by_checkbox("會員積點"),
                False,
            )

    @allure.story("刪除房價-未選擇任一筆")
    def test_remove_rate_cod_not_select(self):
        pages = [HeaderComponent, TipComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("查詢房價列表"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.search().sleep(2)
            web.base_page.screenshot("查詢房價列表")

        with allure.step("未選擇任一筆房價點擊刪除"):
            web.base_page.click_toolbar_with_icon("remove").sleep(1)
            web.base_page.screenshot("未選擇任一筆房價點擊刪除")

        with allure.step("驗證提示訊息"):
            web.base_page.assert_data(
                "請選擇一筆資料", web.tip_component.get_tip_text(), "請選擇一筆資料"
            )

    @allure.story("刪除房價-被其他功能使用過")
    @pytest.mark.parametrize(
        "rate_code, tip_msg",
        [
            ("comcon", "此房價代號已於商務公司合約使用，不可刪除"),
            ("comcon2", "此房價有綁訂特殊約,無法刪除"),
            ("Normal", "此房價代號已於訂房卡使用，不可刪除"),
        ],
    )
    def test_remove_rate_cod_limit(self, rate_code, tip_msg):
        pages = [HeaderComponent, TipComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("查詢房價列表"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.set_value_by_label("房價代號", rate_code)
            web.base_page.search().sleep(2)
            web.base_page.screenshot("查詢房價列表")

        with allure.step("選擇無法被刪除的房價點擊刪除"):
            web.base_page.click_target_rate_cod(rate_code)
            web.base_page.click_toolbar_with_icon("remove").sleep(1)
            if rate_code != "comcon2":
                web.tip_component.click_ok().sleep(1)
            web.base_page.screenshot("選擇無法被刪除的房價點擊刪除").sleep(2)

        with allure.step("驗證提示訊息"):
            web.base_page.assert_data("驗證提示訊息", web.tip_component.get_tip_text(), tip_msg)

    # ------ 新增不統計房價 ------

    @allure.story("新增不統計房價")
    @pytest.mark.xdist_group("nst_rate_cod")
    @pytest.mark.dependency(name="test_create_nst_rate_cod", scope="session")
    @pytest.mark.parametrize("rate_code_type", ["NST"])
    def test_create_nst_rate_cod(self, cache, rate_code_type):
        pages = [
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            ServiceItemComponent,
            RateCodDialog,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        rate_cod_step = globals()[f"{rate_code_type}RateCodStep"](web)

        with allure.step("開啟房價新增視窗"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.click_toolbar_with_icon("add").sleep(2)
            web.base_page.screenshot("開啟房價新增視窗")

        with allure.step("填入房價資訊並儲存成功"):
            rate_cod_name = f"{rate_code_type}{RandomHelper.random_string(3)}"
            rate_cod_step.input_rate_cod_info(rate_cod_name)
            rate_cod_step.set_use_duration()
            rate_cod_step.set_rate_cod_price()
            web.rate_cod_dialog.click_data_field_id("save").sleep(2)
            web.base_page.screenshot("填入房價資訊並儲存成功")
            web.tip_component.click_ok().sleep(2)
            rate_cod_step.set_service_items()
            web.rate_cod_dialog.close_panel()

        with allure.step("驗證新增房價資料"):
            cache.set("rate_cod", rate_cod_name[:8])
            web.base_page.set_value_by_label("房價代號", rate_cod_name[:8])
            web.base_page.search().sleep(2)
            web.base_page.click_target_rate_cod(rate_cod_name[:8])
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.screenshot("驗證新增房價資料")
            rate_cod_step.valid_rate_cod_info(rate_cod_name)

    @pytest.mark.xdist_group("nst_rate_cod")
    @pytest.mark.dependency(
        name="test_remove_rate_cod", depends=["test_create_nst_rate_cod"], scope="session"
    )
    @allure.story("刪除房價-刪除一筆房價成功")
    def test_remove_rate_cod(self, cache):
        pages = [HeaderComponent, TipComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        rate_cod = cache.get("rate_cod", "GR_9Ij")

        with allure.step("查詢房價列表"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.set_value_by_label("房價代號", rate_cod)
            web.base_page.search().sleep(2)
            web.base_page.screenshot("查詢房價列表")

        with allure.step("刪除房價成功"):
            web.base_page.click_target_rate_cod(rate_cod)
            web.base_page.click_toolbar_with_icon("remove").sleep(1)
            web.tip_component.click_ok().sleep(1)
            web.base_page.screenshot("刪除房價成功")
            web.tip_component.click_ok().sleep(1)
            web.tip_component.click_ok().sleep(1)

        with allure.step("驗證房價已刪除"):
            web.base_page.search().sleep(2)
            web.base_page.screenshot("驗證房價已刪除")
            web.base_page.assert_data("查無資料", web.tip_component.get_tip_text(), "無符合資料")

    # ------ 新增不統計房價 END ------

    # ------ 新增合約房價 ------
    @allure.story("新增合約房價")
    @pytest.mark.parametrize("rate_code_type", ["Con"])
    @pytest.mark.xdist_group("con_rate_cod")
    @pytest.mark.dependency(name="test_create_con_rate_cod", scope="session")
    def test_create_con_rate_cod(self, cache, rate_code_type):
        pages = [
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            ServiceItemComponent,
            RateCodDialog,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        rate_cod_step = globals()[f"{rate_code_type}RateCodStep"](web)

        with allure.step("開啟房價新增視窗"):
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.click_toolbar_with_icon("add").sleep(2)
            web.base_page.screenshot("開啟房價新增視窗")

        with allure.step("填入房價資訊並儲存成功"):
            rate_cod_name = f"{rate_code_type}{RandomHelper.random_string(3)}"
            rate_cod_step.input_rate_cod_info(rate_cod_name)
            rate_cod_step.set_use_duration()
            rate_cod_step.set_rate_cod_price()
            web.rate_cod_dialog.click_data_field_id("save").sleep(2)
            web.base_page.screenshot("填入房價資訊並儲存成功")
            web.tip_component.click_ok().sleep(2)
            rate_cod_step.set_service_items()
            web.rate_cod_dialog.close_panel()

        with allure.step("驗證新增房價資料"):
            cache.set("con_rate_cod", rate_cod_name)
            web.base_page.set_value_by_label("房價代號", rate_cod_name[:8])
            web.base_page.search().sleep(2)
            web.base_page.click_target_rate_cod(rate_cod_name[:8])
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.screenshot("驗證新增房價資料")
            rate_cod_step.valid_rate_cod_info(rate_cod_name)

    @allure.story("商務公司綁定公司約")
    @pytest.mark.xdist_group("con_rate_cod")
    @pytest.mark.dependency(
        name="test_contract_bind_rate_cod", depends=["test_create_con_rate_cod"], scope="session"
    )
    def test_contract_bind_rate_cod(self, cache):
        pages = [
            HeaderComponent,
            TipComponent,
            CompanyPanelComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        con_rate_cod = cache.get("con_rate_cod", "Con_YeM")

        with allure.step("查詢公司編號"):
            web.header_component.expand_menu("業務")
            web.header_component.to_func_page("商務公司").sleep(2)
            web.base_page.set_value_by_label("公司編號", "0000173701")
            web.base_page.search().sleep(2)
            web.base_page.screenshot("查詢公司編號")

        with allure.step("商務公司刪除舊綁定"):
            web.base_page.click_target_ikey_3("0000173701")
            web.base_page.click_toolbar_with_icon("edit").sleep(1)
            web.share_panel_component.click_detail_tab("contract").sleep(1)
            web.company_panel_component.click_target_contract()
            web.company_panel_component.click_remove_contract().sleep(1)
            web.tip_component.click_btn_by_text("確定").sleep(1)
            web.company_panel_component.click_save().sleep(2)
            web.tip_component.click_ok().sleep(1)
            web.base_page.click_target_ikey_3("0000173701")
            web.base_page.click_toolbar_with_icon("edit").sleep(1)
            web.share_panel_component.click_detail_tab("contract").sleep(1)
            web.share_panel_component.screenshot("商務公司刪除舊綁定")

        with allure.step("填寫商務公司綁定資料"):
            web.company_panel_component.click_add_contract().sleep(1)
            web.company_panel_component.setting_contract(
                contract_no="1",
                start_date="2024/01/17",
                end_date="2024/01/27",
                hotel_cod="01 : 台北總公司及建設事業",
                con_rate_cod=f"{con_rate_cod[:8]}:{con_rate_cod}",
            )
            web.share_panel_component.screenshot("填寫商務公司綁定資料")

        with allure.step("儲存商務公司綁定資料成功"):
            web.company_panel_component.click_save().sleep(2)
            web.share_panel_component.screenshot("儲存商務公司綁定資料成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("驗證商務公司綁定資料"):
            web.base_page.click_target_ikey_3("0000173701")
            web.base_page.click_toolbar_with_icon("edit").sleep(1)
            web.share_panel_component.click_detail_tab("contract").sleep(1)
            web.share_panel_component.screenshot("驗證商務公司綁定資料")
            web.company_panel_component.assert_data(
                "綁定合約-合約編號",
                web.company_panel_component.get_td_input_value("contract_cod"),
                "1",
            )
            web.company_panel_component.assert_data(
                "綁定合約-開始日期",
                web.company_panel_component.get_td_input_value("begin_dat"),
                "2024/01/17",
            )
            web.company_panel_component.assert_data(
                "綁定合約-結束日期",
                web.company_panel_component.get_td_input_value("end_dat"),
                "2024/01/27",
            )
            web.company_panel_component.assert_data(
                "綁定合約-館別",
                web.company_panel_component.get_td_input_value("hotel_cod"),
                "01 : 台北總公司及建設事業",
            )
            web.company_panel_component.assert_data(
                "綁定合約-房價代號",
                web.company_panel_component.get_td_input_value("rate_cod"),
                f"{con_rate_cod[:8]} : {con_rate_cod}",
            )
            web.company_panel_component.assert_data(
                "綁定合約-訂房來源",
                web.company_panel_component.get_td_input_value("source_typ"),
                "01 : 簽約客戶",
            )
            web.company_panel_component.assert_data(
                "綁定合約-市場類別",
                web.company_panel_component.get_td_input_value("guest_typ"),
                "FIT : 散客",
            )
            web.share_panel_component.close_panel("商務公司維護")

    @allure.story("商務公司綁定特殊約")
    @pytest.mark.xdist_group("con_rate_cod")
    @pytest.mark.dependency(
        name="test_special_contract_bind_rate_cod",
        depends=["test_contract_bind_rate_cod"],
        scope="session",
    )
    def test_special_contract_bind_rate_cod(self, cache):
        pages = [
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            CompanyPanelComponent,
            BasePage,
            RateCodDialog,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        con_rate_cod = cache.get("con_rate_cod", "Con_QdF")

        web.header_component.expand_menu("業務")
        web.header_component.to_func_page("商務公司").sleep(2)
        web.base_page.set_value_by_label("公司編號", "0000173701")
        web.base_page.search().sleep(2)
        web.base_page.click_target_ikey_3("0000173701")
        web.base_page.click_toolbar_with_icon("edit").sleep(1)
        web.share_panel_component.click_detail_tab("specialContract").sleep(1)

        with allure.step("刪除舊特殊約"):
            try:
                web.company_panel_component.click_remove_special_contract()
                web.tip_component.click_ok().sleep(1)
                web.share_panel_component.screenshot("刪除舊特殊約")
            except NoSuchElementException:
                print("舊特殊約不存在")

        with allure.step("業務公司綁定公司約"):
            web.company_panel_component.click_add_special_contract().sleep(1)
            web.company_panel_component.select_special_rate_cod(con_rate_cod).sleep(1)
            web.company_panel_component.screenshot("業務公司綁定公司約")

        with allure.step("設定特殊約金額"):
            web.rate_cod_dialog.click_tab("roomRent").sleep(1)
            web.rate_cod_dialog.input_values_by_row("roomRent", "假日", [1000, 1000])
            web.rate_cod_dialog.input_values_by_row("roomRent", "平日", [500, 500])
            web.rate_cod_dialog.screenshot("設定特殊約金額-房型")
            web.rate_cod_dialog.click_tab("addAdult").sleep(1)
            web.rate_cod_dialog.input_values_by_row("addAdult", "假日", [100, 100])
            web.rate_cod_dialog.input_values_by_row("addAdult", "平日", [50, 50])
            web.rate_cod_dialog.screenshot("設定特殊約金額-加大人")
            web.rate_cod_dialog.click_tab("addChild").sleep(1)
            web.rate_cod_dialog.input_values_by_row("addChild", "假日", [50, 50])
            web.rate_cod_dialog.input_values_by_row("addChild", "平日", [25, 25])
            web.rate_cod_dialog.screenshot("設定特殊約金額-加小孩")

            web.rate_cod_dialog.click_data_field_id("save").sleep(2)
            web.tip_component.click_ok().sleep(1)
            web.rate_cod_dialog.screenshot("設定特殊約金額-儲存成功")

        with allure.step("驗證特殊約綁定成功"):
            web.rate_cod_dialog.close_panel()
            web.share_panel_component.close_panel("商務公司維護")
            web.header_component.expand_menu("訂房")
            web.header_component.to_func_page("房價").sleep(2)
            web.base_page.set_value_by_label("房價代號", con_rate_cod)
            web.base_page.search().sleep(2)
            web.base_page.click_target_rate_cod(con_rate_cod)
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.rate_cod_dialog.click_tab("specialContract").sleep(1)
            web.rate_cod_dialog.screenshot("驗證特殊約綁定成功")
            web.rate_cod_dialog.assert_data(
                "相關特殊約", web.rate_cod_dialog.has_cratecod_mn("BB測測"), True
            )

    # ------ 新增合約房價 END ------
