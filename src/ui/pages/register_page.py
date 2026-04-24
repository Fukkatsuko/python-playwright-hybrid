import allure
from playwright.sync_api import Page, expect

from src.ui.pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_field = self.page.get_by_placeholder("Username")
        self.email_field = self.page.get_by_placeholder("Email")
        self.password_field = self.page.get_by_placeholder("Password")
        self.register_button = self.page.get_by_role("button", name="Sign up")

    def registration(self, username, email, password):
        with allure.step(f"Login with user: {username}"):
            self.username_field.fill(username)
            self.email_field.fill(email)
            self.password_field.fill(password)
            if self.register_button.is_enabled():
                self.register_button.click()

    @allure.step("Check that Login button disable")
    def register_button_disabled(self):
        expect(self.register_button).to_be_disabled()
