import re

import allure
from playwright.sync_api import Page, expect

from src.ui.pages.base_page import BasePage


class ArticlePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.comment_field = self.page.get_by_placeholder("Write a comment...")
        self.comment_button = self.page.get_by_role("button", name="Post Comment")
        self.comments = self.page.locator("app-article-comment")

        self.favorite_button = self.page.locator(".article-actions").get_by_role("button", name=re.compile(r"Favorite",
                                                                                                           re.I)).first
        self.favorite_counter = self.page.locator(".article-actions .counter")
        self.edit_button = self.page.get_by_role("link", name=re.compile(r"Edit Article", re.IGNORECASE))
        self.delete_button = self.page.get_by_role("button", name=re.compile(r"Delete Article", re.IGNORECASE))

        self.article_title = self.page.get_by_role("heading", level=1)
        self.article_text = self.page.locator(".col-md-12")
        self.article_tags = self.page.locator(".tag-list")

    def leave_comment(self, text):
        with allure.step("Leave comment"):
            self.comment_field.fill("")
            self.comment_field.fill(text)
            self.comment_button.click()
            expect(self.comment_field).to_be_empty()

    @allure.step("Add this article to favorites")
    def get_article_to_favorite(self):
        self.favorite_button.first.click()
        expect(self.favorite_button).to_have_class(re.compile(r"btn-primary"))

    @allure.step("Click the edit article button")
    def click_edit_article(self):
        self.edit_button.first.click()
        expect(self.page).to_have_url(re.compile(r".*/editor/.*"))

    @allure.step("Delete article")
    def delete_article(self):
        self.delete_button.first.click()
        expect(self.page).to_have_url(re.compile(r".*realworld.show.*"))

    def check_attributes_of_article(self, article_title, article_text, tag_name):
        with allure.step("Check attributes of article"):
            expect(self.article_title).to_contain_text(article_title)
            expect(self.article_text).to_contain_text(article_text)
            expect(self.article_tags).to_contain_text(tag_name)
