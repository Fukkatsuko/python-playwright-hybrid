import re

import allure
import pytest
from faker.generator import random
from playwright.sync_api import expect


@pytest.mark.hybrid
@allure.feature("Hybrid: Articles")
@allure.story("Article flow")
class TestArticleFlow:

    @pytest.mark.flaky(reruns=3)
    @allure.title("Article life cycle")
    @pytest.mark.parametrize("title, description, body, tags", [
        ("New title", "New description", "New text", ["new"])
    ])
    def test_article_flow(self, auth_user, conduit_api, article_creation_page, main_page, article_page,
                          title, description, body, tags):
        main_page.visit("/")

        with allure.step("Create article"):
            main_page.click_new_article_button()
            expect(article_creation_page.page).to_have_url(re.compile(r".*/editor"))
            article_creation_page.create_article(title, description, body, tags[0])

        with allure.step("Check created article"):
            expect(article_page.page).to_have_url(re.compile(r".*/article/.*"))
            article_page.check_attributes_of_article(title, body, tags[0])
            slug = article_page.page.url.split('/')[-1]

        with allure.step("Edit article"):
            article_page.click_edit_article()

            rand_id = random.randint(100, 999)
            updated_data = {
                "title": f"{title} UPD {rand_id}",
                "description": f"{description} UPD {rand_id}",
                "body": f"{body} UPD {rand_id}",
                "tags": "updated-tag"
            }

            article_creation_page.edit_article(
                title=updated_data["title"],
                description=updated_data["description"],
                text=updated_data["body"],
                tags=updated_data["tags"]
            )

            expect(article_page.page).not_to_have_url(re.compile(f".*/article/{slug}$"), timeout=15000)
            article_page.page.wait_for_timeout(2000)
            expect(article_page.article_title).to_have_text(updated_data["title"], timeout=10000)

            slug_new = article_page.page.url.split('/')[-1]

        with allure.step("Check edited article"):
            article_page.check_attributes_of_article(
                updated_data["title"],
                updated_data["body"],
                updated_data["tags"]
            )

        with allure.step("Check article on Main Page"):
            main_page.visit("/")
            expect(main_page.page.get_by_role("heading", name=updated_data["title"])).to_be_visible()
            expect(main_page.page.get_by_text(updated_data["description"])).to_be_visible()

        with allure.step("Delete article"):
            article_page.visit(f"/article/{slug_new}")
            article_page.delete_article()
            expect(article_page.page).to_have_url(re.compile(r".*realworld.show.*"))
            expect(main_page.page.get_by_role("heading", name=updated_data["title"])).not_to_be_visible()

        with allure.step("Verify deletion via API"):
            response = conduit_api.articles.get_article(slug_new)
            assert response.status_code == 404

    @allure.title("Click to logo on article page")
    def test_logo_click_from_article_page(self, auth_user, api_article, article_page, main_page):
        slug = api_article["slug"]

        with allure.step(f"Transition by a logged-in user to the editor of someone else's article: {slug}"):
            article_page.page.goto(f"/article/{slug}")

        with allure.step(f"Clicks on the logo"):
            article_page.logo.click()

        with allure.step("Checking the redirect to the main page"):
            expect(main_page.page).not_to_have_url(re.compile(r".*/article/*"))
            expect(main_page.page).to_have_url(re.compile(r".*realworld.show.*"))

    @allure.title("Liking article")
    def test_liking_article(self, auth_user, article_page, main_page):
        main_page.visit("/")

        with allure.step("Jump to the first article from the 'Global Feed' list"):
            main_page.click_the_first_article_in_global_feed()
            initial_likes = int(article_page.favorite_counter.inner_text()[1])

        with allure.step(f"Like article"):
            article_page.get_article_to_favorite()

        with allure.step("UI Verify: Checking that a button has changed state"):
            expect(article_page.favorite_button).to_contain_text(f"Unfavorite Article ({initial_likes + 1})")
            expect(article_page.favorite_button).to_have_class(re.compile(r"btn-primary"))
