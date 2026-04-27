import re

import allure
from playwright.sync_api import Page, expect

from src.ui.pages.base_page import BasePage


class ArticleCreationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title_field = self.page.get_by_placeholder("Article Title")
        self.description_field = self.page.get_by_placeholder("What's this article about?")
        self.text_field = self.page.get_by_placeholder("Write your article (in markdown)")
        self.tags_field = self.page.get_by_placeholder("Enter tags")
        self.save_button = self.page.get_by_role("button", name="Publish Article")
        self.error_messages = self.page.locator(".error-messages")

    def create_article(self, title=None, description=None, text=None, tags=None):
        with allure.step("Create article"):
            if title is not None:
                self.title_field.fill(title)
            if description is not None:
                self.description_field.fill(description)
            if text is not None:
                self.text_field.fill(text)
            if tags:
                self.tags_field.fill(tags)
                self.tags_field.press("Enter")
            self.save_button.click()
            if all([title, description, text]):
                expect(self.save_button).not_to_be_visible()
                expect(self.page).to_have_url(re.compile(r".*/article/.*"))

    def _clear_and_fill(self, locator, value):
        locator.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.press("Backspace")
        locator.fill(value)

    def edit_article(self, title=None, description=None, text=None, tags=None):
        with allure.step("Edit article fields"):
            if title:
                self._clear_and_fill(self.title_field, title)
            if description:
                self._clear_and_fill(self.description_field, description)
            if text:
                self._clear_and_fill(self.text_field, text)
            if tags:
                self.tags_field.fill(tags)
                self.tags_field.press("Enter")

            self.page.locator("body").click()
            self.save_button.wait_for(state="visible")
            self.save_button.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)
            self.save_button.click()
            if all([title, description, text]):
                expect(self.save_button).not_to_be_visible()
                expect(self.page).not_to_have_url(re.compile(r".*/editor/.*"), timeout=15000)

    @allure.step("Checking article validation error: {text}")
    def check_validation_error(self, text):
        expect(self.error_messages).to_contain_text(text)
        expect(self.page).to_have_url(re.compile(r".*/editor.*"))
