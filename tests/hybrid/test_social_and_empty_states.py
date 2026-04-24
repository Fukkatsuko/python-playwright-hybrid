import allure
import pytest
from faker.generator import random
from playwright.sync_api import expect

from utils.generators import generate_article_data


@pytest.mark.hybrid
@allure.feature("Hybrid: Social interaction")
@allure.story("Test social and empty states")
class TestSocialNEmptyStates:

    @allure.title("Leave a comment and count them")
    def test_comment_counter(self, auth_user, api_article, article_page, conduit_api):
        slug = api_article["slug"]

        with allure.step(f"Transition by a logged-in user to the editor of someone else's article: {slug}"):
            article_page.page.goto(f"/article/{slug}")
            comment_count = int(article_page.comments.count())

        with allure.step(f"UI: add comment"):
            comment_text = "This is comment for this article"
            article_page.leave_comment(comment_text)

        with allure.step(f"UI: check counter"):
            expect(article_page.comments).to_have_count(comment_count + 1)

        with allure.step("API Verify: Checking if a comment is saved on the server"):
            response = conduit_api.articles.get_comments(slug)
            assert response.status_code == 200

            comments_list = response.json()["comments"]
            assert comments_list[0]["body"] == comment_text
            assert len(comments_list) == comment_count + 1

    @allure.title("Checking for an empty article list in main page")
    def test_empty_article_list_main_page(self, auth_user, conduit_api, main_page):
        unique_tag = f"tag_{random.randint(1000, 9999)}"
        data = generate_article_data()
        data["article"]["tagList"] = [unique_tag]

        with allure.step("Create and delete article"):
            resp = conduit_api.articles.create_article(data)
            slug = resp.json()["article"]["slug"]
            title = resp.json()["article"]["title"]

        with allure.step("Check created article in main page"):
            main_page.visit("/")
            expect(main_page.page.get_by_role("heading", name=title)).to_be_visible(timeout=10000)

        with allure.step("delete article"):
            conduit_api.articles.delete_article(slug)

        with allure.step("Go to tag page"):
            main_page.visit(f"/tag/{unique_tag}")

        with allure.step(f"Checking empty feed message for tag {unique_tag}"):
            expect(main_page.empty_feed_message).to_be_visible(timeout=10000)

    @allure.title("Checking for an empty article list in user's profile")
    def test_empty_article_list_profile(self, auth_user, conduit_api, profile_page):
        res = conduit_api.users.get_current_user()
        username = res.json()["user"]["username"]

        with allure.step(f"Go to profile user {username} without articles"):
            profile_page.page.goto(f"/profile/{username}")

        with allure.step(f"Checking empty feed message in profile user {username} without articles"):
            expect(profile_page.empty_feed_message).to_be_visible(timeout=10000)
