from pages.athena_base_page import AthenaBasePage
from locators.transport_services_locator import TransportServicesLocator


class TransportServicesComponent(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, TransportServicesLocator())

    def set_transport_service(self, fee=None, transport_type=None):
        if transport_type:
            transport_status_locator = self.format_locator(
                self.locator.transport_field_combobox_text, "接/送"
            )
            self.click(transport_status_locator)
            transport_option_locator = self.format_locator(
                self.locator.transport_type_option, transport_type
            )
            self.click(transport_option_locator)
            # 等待 combobox 顯示所選的接送方式（選項註冊完成的實際條件）
            self.wait_until(
                lambda d: transport_type
                in (d.find_element(*transport_status_locator).get_attribute("value") or "")
            )

        if fee is not None:
            self.click(self.locator.transport_auto_charge_checkbox)
            fee_locator = self.format_locator(self.locator.transport_field_spinbutton, "費用")
            self.input_with_clear(fee_locator, fee)
        time_locator = self.format_locator(self.locator.transport_field_with_div, "時間")
        self.click(time_locator)
        self.click(self.locator.transport_time_confirm_btn)
        return self

    def get_transport_field_value(self, field_name):
        """取得接送服務表單欄位值 (帶 div 包裹的 input)"""
        locator = self.format_locator(self.locator.transport_field_with_div, field_name)
        return self.driver.find_element(*locator).get_attribute("value")

    def get_transport_field_direct_value(self, field_name):
        """取得接送服務表單欄位值 (直接跟在 div 後的 input)"""
        locator = self.format_locator(self.locator.transport_field_direct, field_name)
        return self.driver.find_element(*locator).get_attribute("value")

    def get_transport_combobox_text(self, field_name):
        """取得接送服務 combobox 的顯示文字 (如：A : 接)"""
        locator = self.format_locator(self.locator.transport_field_combobox_text, field_name)
        return self.driver.find_element(*locator).get_attribute("value")

    def get_transport_spinbutton_value(self, field_name):
        """取得接送服務數字欄位值"""
        locator = self.format_locator(self.locator.transport_field_spinbutton, field_name)
        return self.driver.find_element(*locator).get_attribute("value")

    def get_transport_grid_cell_text(self, column_index):
        """取得接送服務 Grid 表格欄位文字"""
        locator = self.format_locator(self.locator.transport_grid_cell, column_index)
        return self.driver.find_element(*locator).text

    def get_transport_grid_cell_text_by_row(self, row_index, column_index):
        """取得接送服務表格指定行和列的文字"""
        locator = self.format_locator(
            self.locator.transport_data_colume_by_row_and_index, (row_index, column_index)
        )
        return self.driver.find_element(*locator).text

    def click_transport_grid_last_row(self):
        """點擊接送服務表格的最後一筆資料"""
        self.click(self.locator.transport_grid_last_row)
        return self

    def click_transport_grid_row(self, index):
        """點擊接送服務表格的指定列資料"""
        locator = self.format_locator(self.locator.transport_data_row_by_index, str(index))
        self.click(locator)
        return self

    def click_transport_batch_add(self):
        self.click(self.locator.btn_batch_add_transport)
        return self

    def click_save_transport_batch(self):
        self.click(self.locator.btn_save_batch_add_transport)
        return self

    def get_transport_row_count(self):
        """取得接送服務表格的資料筆數"""
        transport_count = len(self.driver.find_elements(*self.locator.transport_data_rows))
        return transport_count

    def has_transport_service(self):
        return self.driver.find_elements(*self.locator.transport_grid_last_row)
