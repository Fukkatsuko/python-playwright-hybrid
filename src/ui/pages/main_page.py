import re

import allure
from playwright.sync_api import Page, expect

from src.ui.pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_link = self.page.get_by_role("link", name="Sign in")
        self.register_link = self.page.get_by_role("link", name="Sign up")
        self.global_feed_tab = self.page.locator(".feed-toggle").get_by_text("Global Feed")
        self.first_article_link = self.page.locator(".article-preview").first.locator(".preview-link")

        self.new_post_link = self.page.get_by_role("link", name="New Article")
        self.setting_link = self.page.get_by_role("link", name="Settings")

        self.empty_feed_message = self.page.get_by_text("No articles are here... yet.")

        self.tags = self.page.locator(".tag-list a")
        self.active_tag_tab = self.page.locator(".feed-toggle .nav-item .nav-link.active")


    @allure.step("Click the 'New Article' button in the header")
    def click_new_article_button(self):
        self.new_post_link.click()

    @allure.step("Click the 'Settings' button in the header")
    def click_settings_button(self):
        self.setting_link.click()

    def click_first_tag_and_verify(self):
        tag_name = self.tags.first.inner_text()

        with allure.step(f"Click on the tag: {tag_name}"):
            self.tags.first.click()

        with allure.step(f"Checking that the {tag_name} tab is now active"):
            expect(self.active_tag_tab).to_contain_text(tag_name)

    def click_the_first_article_in_global_feed(self):
        expect(self.first_article_link).to_be_visible()
        article_title = self.first_article_link.inner_text()

        with allure.step(f"Click on the first article: '{article_title}'"):
            self.first_article_link.click()

        with allure.step(f"Checking that the article has opened"):
            expect(self.page).to_have_url(re.compile(r".*/article/.*"))
