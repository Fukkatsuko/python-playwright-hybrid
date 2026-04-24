import allure
import pytest


@pytest.mark.ui
@allure.feature("UI: Articles")
@allure.story("Create article")
class TestArticleEditor:

    @allure.title("Create article with empty fields")
    @pytest.mark.parametrize("title, description, body, errors", [
        ("Article", "description", "", ["body can't be blank"]),
        ("", "description", "Text of the Article", ["title can't be blank"]),
        ("Article", "", "Text of the Article", ["description can't be blank"]),
        ("", "", "", [
            "title can't be blank",
            "description can't be blank",
            "body can't be blank"
        ])
    ])
    def test_article_empty_fields_validation(self, editor_page, title, description, body, errors):
        with allure.step(f"Create an article with data: {title}, {description}, {body}"):
            editor_page.create_article(title, description, body)

        with allure.step("Checking for all expected error messages"):
            for error in errors:
                editor_page.check_validation_error(error)
