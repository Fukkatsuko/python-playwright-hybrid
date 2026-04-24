import re

import allure
import pytest
from playwright.sync_api import expect


@pytest.mark.ui
@allure.feature("UI: Navigation")
@allure.story("Interaction with the logo")
class TestNavigation:

    @allure.title("Click on the logo from the registration and login pages")
    @pytest.mark.parametrize("page_fixture, url", [
        ("login_page", "/login"),
        ("register_page", "/register")
    ])
    def test_logo_guest_pages(self, request, page_fixture, url):
        with allure.step(f"An unauthorized user goes to page {url} and clicks on the logo"):
            current_page = request.getfixturevalue(page_fixture)
            current_page.visit(url)
            current_page.logo.click()
        with allure.step("Checking the redirect to the main page"):
            expect(current_page.page).not_to_have_url(re.compile(url))
            expect(current_page.page).to_have_url(re.compile(r".*realworld.show.*"))

    @allure.title("Click on the logo from the user settings and article creation pages")
    @pytest.mark.parametrize("page_fixture, url", [
        ("settings_page", "/settings"),
        ("article_creation_page", "/editor")
    ])
    def test_logo_auth_pages(self, request, auth_user, page_fixture, url):
        with allure.step(f"An authorized user goes to page {url} and clicks on the logo"):
            current_page = request.getfixturevalue(page_fixture)
            current_page.visit(url)
            current_page.logo.click()
        with allure.step("Checking the redirect to the main page"):
            expect(current_page.page).not_to_have_url(re.compile(url))
            expect(current_page.page).to_have_url(re.compile(r".*realworld.show.*"))
