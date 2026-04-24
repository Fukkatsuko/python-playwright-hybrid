import allure
import pytest


@pytest.mark.ui
@allure.feature("UI: Login Page")
@allure.story("Validation the login form")
class TestLoginValidation:

    @allure.title("Login with invalid email format")
    @pytest.mark.parametrize("invalid_email", [
        "test_at_mail.com",  # without @
        "test@mail",  # without domain
        "@@mail.com"  # extra characters
    ])
    def test_login_invalid_email_format(self, login_page, invalid_email):
        login_page.visit("/login")

        with allure.step(f"Attempt to login with email: {invalid_email}"):
            login_page.login(invalid_email, "some_password")

        login_page.check_error_message("credentials invalid")

    @allure.title("Login with empty fields")
    @pytest.mark.parametrize("email, password", [
        ("", "password123"),
        ("test@mail.com", ""),
        ("", "")
    ])
    def test_login_empty_fields_validation(self, login_page, email, password):
        login_page.visit("/login")
        login_page.login(email, password)
        login_page.login_button_disabled()

    @allure.title("Login with non-existent user")
    def test_login_non_existent_user_login(self, login_page):
        login_page.visit("/login")
        login_page.login("never_exists_12345@mail.com", "wrong_password")
        login_page.check_error_message("credentials invalid")

    @allure.title("Login with invalid password")
    @pytest.mark.parametrize("invalid_password", [
        "pas1",  # less than 8
        "wrong_password"  # wrong password for current user
    ])
    def test_login_invalid_password(self, login_page, invalid_password):
        login_page.visit("/login")

        with allure.step(f"Attempt to login with password: {invalid_password}"):
            login_page.login("valid_format@mail.com", invalid_password)

        login_page.check_error_message("credentials invalid")
