from playwright.sync_api import Playwright, sync_playwright, expect


class WebDriver:
    def __init__(self, page_object=None):
        # self.page = page_object
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False, slow_mo=500)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()


    def open_url(self, url):
        self.page.goto(url)