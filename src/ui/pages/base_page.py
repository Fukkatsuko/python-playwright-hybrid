import allure
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logo = self.page.locator(".navbar-logo")
        self.error_messages = self.page.locator(".error-messages")

    def visit(self, url: str):
        with allure.step(f"Opening page: {url}"):
            self.page.goto(url)

    @allure.step("Checking validation error: {text}")
    def check_error_message(self, text):
        expect(self.error_messages).to_contain_text(text)
