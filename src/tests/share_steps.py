from tools.random_helper import RandomHelper


class ShareSteps:

    @staticmethod
    def open_shift(web, hall_type, shift, pw):  # 開班
        web.share_panel_component.select_by_label("廳別", hall_type)
        web.share_panel_component.input_by_label("班別", shift)
        web.share_panel_component.input_by_label("密碼", pw)
        web.share_panel_component.click_panel_footer_btn("開班", "確認")
        web.tip_component.click_ok().sleep(2)

    @staticmethod
    def to_reservation_detail(web, menu, func_name, search_cond, search_value, toolbar):
        # 訂房卡頁面 > 訂房明細
        web.header_component.expand_menu(menu).sleep(1)
        web.header_component.to_func_page(func_name).sleep(1)
        web.reservation_card_dialog.search_reservation_card(search_cond, search_value).sleep(1)
        web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
        web.reservation_card_dialog.click_card_toolbar(toolbar).sleep(1)

    @staticmethod
    def create_or_enter_reservation_detail(
        web,
        search_cond,
        search_value,
        toolbar,
        first_name=None,
        last_name=None,
        rate_cod_name=None,
        room_type=None,
    ):
        # 訂房卡頁面查詢 > 無訂房卡則建立訂房卡並進入明細 or 有訂房卡直接進入訂房明細
        web.header_component.expand_menu("訂房").sleep(1)
        web.header_component.to_func_page("訂房卡").sleep(1)

        web.reservation_card_dialog.search_reservation_card(search_cond, search_value).sleep(1)
        if web.reservation_card_dialog.has_reservation_card():
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
        else:
            web.reservation_card_dialog.click_btn_add().sleep(1)
            web.reservation_page.click_edit_guest().sleep(3)
            web.reservation_page.create_guest(
                first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
            )
            web.tip_component.click_ok().sleep(1)
            web.reservation_card_dialog.click_edit_rate_cod()
            web.reservation_card_dialog.set_rate_code(rate_cod_name, room_type).sleep(1)
            web.reservation_page.save_card()
            web.tip_component.click_ok().sleep(2)

        web.reservation_card_dialog.click_card_toolbar(toolbar).sleep(3)

    @staticmethod
    def verify_save_success_tip(web, message=None):  # 顯示'儲存成功'提示
        if message:
            web.athena_base_page.screenshot(f"Then 顯示'{message}'提示")
            web.athena_base_page.assert_data(message, web.tip_component.get_tip_text(), message)
        else:
            web.athena_base_page.screenshot("Then 顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
        web.tip_component.click_ok()

    @staticmethod
    def click_btn_save(web, save_method=None):  # 點擊[橘色磁碟片]進行儲存
        if save_method:
            save_method()
        else:
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
        web.athena_base_page.screenshot("And 點擊儲存")
