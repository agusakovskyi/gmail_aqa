import pytest
from utils.gmail_utils import GmailUtils

class TestGmail:
    @pytest.fixture(autouse=True)
    def _initiate_class(self):
        self.gmail_utils = GmailUtils()


    def test_write_letters(self):
        self.gmail_utils.open_gmail()
        self.gmail_utils.login_gmail()
        self.gmail_utils.delete_all_messages()
        self.gmail_utils.send_letters_in_loop()
        self.gmail_utils.collect_data_from_emails()
        self.gmail_utils.send_letter_with_collected_data()
        self.gmail_utils.delete_letters_except_last_one()
    #     context.close()
    #     browser.close()

