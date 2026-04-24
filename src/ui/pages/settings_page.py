import allure
from playwright.sync_api import Page, expect

from src.ui.pages.base_page import BasePage


class SettingsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_field = self.page.get_by_placeholder("Username")
        self.email_field = self.page.get_by_placeholder("Email")
        self.password_field = self.page.get_by_placeholder("New Password")
        self.bio_field = self.page.get_by_placeholder("Short bio about you")
        self.image_field = self.page.get_by_placeholder("URL of profile picture")

        self.save_button = self.page.get_by_role("button", name="Update Settings")
        self.logout_button = self.page.get_by_role("button", name="Or click here to logout.")

    @allure.step("Logout")
    def logout(self):
        self.logout_button.click()
        expect(self.logout_button).not_to_be_visible()

    def change_user_info(self, username=None, email=None, password=None, bio=None, image=None):
        with allure.step(f"Change user info"):
            if username is not None:
                self.username_field.fill(username)
            if email is not None:
                self.email_field.fill(email)
            if password:
                self.password_field.fill(password)
            if bio:
                self.bio_field.fill(bio)
            if image:
                self.image_field.fill(image)
            self.save_button.click()
