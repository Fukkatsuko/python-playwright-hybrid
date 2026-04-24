import allure
from playwright.sync_api import Page, expect

from src.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_field = self.page.get_by_placeholder("Email")
        self.password_feild = self.page.get_by_placeholder("Password")
        self.login_button = self.page.get_by_role("button", name="Sign in")

    def login(self, email, password):
        with allure.step(f"Login with user: {email}"):
            self.email_field.fill(email)
            self.password_feild.fill(password)
            if self.login_button.is_enabled():
                self.login_button.click()

    @allure.step("Check that Login button disable")
    def login_button_disabled(self):
        expect(self.login_button).to_be_disabled()
