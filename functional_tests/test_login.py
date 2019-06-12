from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'emlliuxiang@163.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # 用户访问主页，在邮件登录输入框输入并回车
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # 出现一条信息，提醒用户邮件已发出
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            # 下一行输出的数据类似 'Superlists\nEnter email to log in:\nStart a new To-Do list'
            self.browser.find_element_by_tag_name('body').text
        ))

        # 查看邮件，看到一条信息
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # 邮件中有个URL链接
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 用户点击链接
        self.browser.get(url)

        # 用户登录
        self.wait_to_be_logged_in(email=TEST_EMAIL)
        # self.wait_for(
        #     lambda: self.browser.find_element_by_link_text('Log out')
        # )
        # navbar = self.browser.find_element_by_css_selector('.navbar')
        # self.assertIn(TEST_EMAIL, navbar.text)

        # 现在用户要退出
        self.browser.find_element_by_link_text('Log out').click()

        # 用户退出了
        self.wait_to_be_logged_out(email=TEST_EMAIL)
        # self.wait_for(
        #     lambda: self.browser.find_element_by_name('email')
        # )
        # navbar = self.browser.find_element_by_css_selector('.navbar')
        # self.assertNotIn(TEST_EMAIL, navbar.text)