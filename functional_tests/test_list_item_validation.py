from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # input empty and return error msg
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # self.wait_for(
        #     lambda: self.assertEqual(
        #         self.browser.find_element_by_css_selector('.has-error').text,
        #         "You can't have an empty list item"
        #     )
        # )
        # 浏览器截获了页面，清单页面不会加载
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector(
                    '#id_text:invalid'
            )
        )

        # input valid and done
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # input empty again
        self.get_item_input_box().send_keys(Keys.ENTER)
        # self.wait_for(
        #     lambda: self.assertEqual(
        #         self.browser.find_element_by_css_selector('.has-error').text,
        #         "You can't have an empty list item"
        #     )
        # )
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector(
                    '#id_text:invalid'
            )
        )

        # input valid then ok

        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Make tea')




