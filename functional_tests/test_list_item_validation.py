from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

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

    def test_cannot_add_duplicate_items(self):
        # visit home page and add a list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        # and input a duplicate item
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # then user will see a help message
        self.wait_for(lambda: self.assertEqual(self.get_error_element().text,
                                               "You've already got this in your list"))

    def test_error_messages_are_cleaned_on_input(self):
        # user create a new list and occur a validation error
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # in order to cleanse the error, user input again
        self.get_item_input_box().send_keys('a')

        # the error disappeared
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))



