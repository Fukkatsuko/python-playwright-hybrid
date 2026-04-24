import re

import allure
import pytest
from playwright.sync_api import expect


@pytest.mark.ui
@allure.feature("UI: Content")
@allure.story("Check tags and comments of Article")
class TestContentVisibility:

    @allure.title("Checking guest rights: buttons in the header")
    def test_guest_navigation_links(self, main_page):
        main_page.visit("/")

        with allure.step("Checking the visibility of login and registration buttons"):
            expect(main_page.login_link).to_be_visible()
            expect(main_page.register_link).to_be_visible()

        with allure.step("Checking for missing authorized user buttons"):
            expect(main_page.new_post_link).not_to_be_visible()
            expect(main_page.setting_link).not_to_be_visible()

    @allure.title("Checking tag filtering under guest")
    def test_guest_tags_navigation(self, main_page):
        main_page.visit("/")
        with allure.step("Checking that the Global Feed is active by default"):
            expect(main_page.global_feed_tab).to_have_class(re.compile(r"active"))

        main_page.click_first_tag_and_verify()

    @allure.title("Disabling comments for unauthorized users")
    def test_guest_cannot_comment(self, main_page, article_page):
        with allure.step("Opening the main page as a guest"):
            main_page.visit("/")

        with allure.step("Jump to the first article from the 'Global Feed' list"):
            main_page.click_the_first_article_in_global_feed()

        with allure.step("Checking that the comment block is not displayed"):
            expect(article_page.comment_field).not_to_be_visible()

        with allure.step("Checking the authorization call"):
            expect(article_page.page.get_by_text(re.compile(r"Sign in or sign up", re.I))).to_be_visible()
