from pages.base_page import BasePage


class MessageEditComponent(BasePage):

    def fill_message_fields(self, message_from, phone_number, message_content):
        locator_from = self.formator_locator(self.locator.message_input_field, "留言者")
        locator_phone = self.formator_locator(self.locator.message_input_field, "連絡電話")

        self.input_with_clear(locator_from, message_from)
        self.input_with_clear(locator_phone, phone_number)
        self.input_with_clear(self.locator.message_textarea_field, message_content)
        return self

    def get_message_field_value(self, field_name):
        if field_name == "留言內容":
            return self.driver.find_element(*self.locator.message_textarea_field).get_attribute(
                "value"
            )
        locator = self.formator_locator(self.locator.message_input_field, field_name)
        return self.driver.find_element(*locator).get_attribute("value")

    def get_message_grid_cell_text(self, column_index):
        locator = self.formator_locator(self.locator.message_grid_cell, column_index)
        return self.driver.find_element(*locator).text

    def click_message_grid_last_row(self):
        self.click(self.locator.message_grid_last_row)
        return self

    def click_add_message(self):
        self.click_toolbar_with_icon("add")
        return self

    def click_delete_message(self):
        self.click_toolbar_with_icon("remove")
        return self

    def message_field_is_enabled(self, field):
        field_locator = self.formator_locator(self.locator.message_input_field, field)
        return self.driver.find_element(*field_locator).get_attribute("disabled")

    def message_textarea_field_is_enabled(self):
        return self.driver.find_element(*self.locator.message_textarea_field).get_attribute(
            "disabled"
        )

    def has_message(self):
        return self.driver.find_elements(*self.locator.message_grid_last_row)
