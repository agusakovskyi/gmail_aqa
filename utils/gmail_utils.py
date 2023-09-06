import time

from utils.web_driver import WebDriver
import random
import string

class GmailUtils:
    def __init__(self, page=None):
        self.custom_webdriver = WebDriver(page)
        self.url = "https://www.google.com/intl/en/gmail/about/"
        self.email_address = "test10010010110@gmail.com"
        self.email_password = "abobaTest"
        self.number_of_mails = 10
        self.received_mails_text = "Received mail on theme "
        self.message_content_text = " with message: "
        self.message_of_quantity = ". It contains: "
        self.subject_of_final_message = "Collected Data"

        self.gmail_logo = "//span[@class='mobile-before-hero-only']"
        self.sign_in_button = "//a[@data-action='sign in']"
        self.email_authentication_input = "//input[@type='email']"
        self.password_authentication_input = "//input[@type='password']"
        self.next_authentication_button = "//button[@data-idom-class='nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']"
        self.number_received_messages = "//div[@class='TO aBP nZ aiq']//div[@class='bsU']"
        self.email_input = "//input[@peoplekit-id='BbVjBd']"
        self.subject_input = "//input[@name='subjectbox']"
        self.message_body_input = "//div[@aria-label='Message Body']"
        self.write_letter_button = "//div[@class='T-I T-I-KE L3']"
        self.send_message_button = "//div[text()='Send']"
        self.back_to_inbox_button = "//div[@title='Back to Inbox']"
        self.subject_content = "//h2[@class='hP']"
        self.body_content = "//div[@class='a3s aiL ']//div[@dir='ltr']"
        self.select_all_messages = "//span[@jslog='170807; u014N:cOuCgd,Kr2w4b;']"
        self.select_last_message = "//div[@class='ae4 aDM nH oy8Mbf']//tbody//tr[1]//div[@role='checkbox']"
        self.delete_selected_messages_button = "//div[@data-tooltip='Delete']"
        self.popup_message_sent = "//span[text()='Message sent']"
        # self.close_popup_icon = "//div[@class='bBe']"


        self.lists_content = {}
        self.collected_data_from_emails = {}


    def get_random_string(self, length):
        source = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(source) for i in range(length)))
        return result_str

    def open_gmail(self):
        self.custom_webdriver.open_url(self.url)
        logo = self.custom_webdriver.page.wait_for_selector(self.gmail_logo)
        assert logo.is_visible(), "The main page was not opened"

    def login_gmail(self):
        self.custom_webdriver.page.locator(self.sign_in_button).click()
        self.custom_webdriver.page.locator(self.email_authentication_input).fill(self.email_address)
        self.custom_webdriver.page.locator(self.next_authentication_button).click()
        self.custom_webdriver.page.locator(self.password_authentication_input).fill(self.email_password)
        self.custom_webdriver.page.locator(self.next_authentication_button).click()
        button_write_letter = self.custom_webdriver.page.wait_for_selector(self.write_letter_button)
        assert button_write_letter.is_visible(), "User is unable to login"

    def write_letter_with_random_text(self):
        self.custom_webdriver.page.locator(self.write_letter_button).focus()
        self.custom_webdriver.page.locator(self.write_letter_button).click()
        self.custom_webdriver.page.locator(self.email_input).fill(self.email_address)
        theme = self.get_random_string(self.number_of_mails)
        self.custom_webdriver.page.locator(self.subject_input).fill(theme)
        body = self.get_random_string(self.number_of_mails)
        self.lists_content[theme] = body
        self.custom_webdriver.page.locator(self.message_body_input).fill(body)
        self.custom_webdriver.page.locator(self.send_message_button).click()
        popup_sending_message = self.custom_webdriver.page.wait_for_selector(self.popup_message_sent)
        assert popup_sending_message.is_visible(), "Message was not sent."

    def send_letters_in_loop(self):
        for _index in range(self.number_of_mails):
            self.write_letter_with_random_text()
        actual_inbox = self.custom_webdriver.page.locator(self.number_received_messages).text_content()
        assert int(actual_inbox) == self.number_of_mails, f"Wrong number of received letters. " \
                                                            f"Expected letters: {self.number_of_mails}. Actual result: {actual_inbox}"

    def collect_data_from_emails(self):
        self.custom_webdriver.page.mouse.move(0, 0)
        for i in range (1, 11):
            self.custom_webdriver.page.locator(f"//div[@class='ae4 aDM nH oy8Mbf']//tbody//tr[{i}]").click()
            theme = self.custom_webdriver.page.locator(self.subject_content).text_content()
            body = self.custom_webdriver.page.locator(self.body_content).text_content()
            self.collected_data_from_emails[theme] = body
            self.custom_webdriver.page.locator(self.back_to_inbox_button).click()
        actual_inbox = self.custom_webdriver.page.locator(self.number_received_messages)
        assert actual_inbox.is_hidden(), "Messages were not reviewed."

    def send_letter_with_collected_data(self):
        self.custom_webdriver.page.locator(self.write_letter_button).click()
        self.custom_webdriver.page.locator(self.email_input).fill(self.email_address)
        full_body = ""
        for theme, body in self.collected_data_from_emails.items():
            quantity_of_lett_and_num = self.counting_letters_and_digits(theme+body)
            full_body = f'{full_body} {self.received_mails_text} {theme} {self.message_content_text} {body}' \
                            f'{self.message_of_quantity}{quantity_of_lett_and_num}\n'
        self.custom_webdriver.page.locator(self.subject_input).fill(self.subject_of_final_message)
        self.custom_webdriver.page.locator(self.message_body_input).fill(full_body)
        self.custom_webdriver.page.locator(self.send_message_button).click()
        popup_sending_message = self.custom_webdriver.page.wait_for_selector(self.popup_message_sent)
        assert popup_sending_message.is_visible(), "Message was not sent."

    def delete_letters_except_last_one(self):
        self.custom_webdriver.page.locator(self.select_all_messages).click()
        self.custom_webdriver.page.locator(self.select_last_message).click()
        self.custom_webdriver.page.locator(self.delete_selected_messages_button).click()

    def counting_letters_and_digits(self, string):
        total_digits = 0
        total_letters = 0
        for s in string:
            if s.isnumeric():
                total_digits += 1
            else:
                total_letters += 1
        result = f"{total_letters} letters, {total_digits} numbers"
        return result

    def delete_all_messages(self):
        actual_inbox = self.custom_webdriver.page.locator(self.number_received_messages)
        if actual_inbox.is_visible():
            self.custom_webdriver.page.locator(self.select_all_messages).click()
            self.custom_webdriver.page.locator(self.delete_selected_messages_button).click()
            act_inbox = self.custom_webdriver.page.wait_for_selector(self.number_received_messages)
            assert act_inbox.is_hidden(), "Messages were not deleted."





