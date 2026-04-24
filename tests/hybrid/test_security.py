import re

import allure
import pytest
from playwright.sync_api import expect


@pytest.mark.hybrid
@allure.feature("Hybrid: Security & Permissions")
@allure.story("Differentiation of access rights")
class TestSecurity:

    @allure.title("Editing someone else's article (Forbidden)")
    def test_edit_strangers_article(self, auth_user, api_article, article_page):
        slug = api_article["slug"]

        with allure.step(f"Transition by a logged-in user to the editor of someone else's article: {slug}"):
            article_page.page.goto(f"/editor/{slug}")

        with allure.step("Checking that access is denied"):
            expect(article_page.page).to_have_url(re.compile(r".*realworld.show.*"))
