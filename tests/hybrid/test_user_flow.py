import re

import allure
import pytest
from faker.generator import random
from playwright.sync_api import expect

from utils.generators import generate_conduit_user


@pytest.mark.hybrid
@allure.feature("Hybrid: Users")
@allure.story("Profile Settings")
class TestUserFlow:

    @allure.title("Change user info")
    @pytest.mark.parametrize("username, email, password, bio, image", [
        ("NewUser", f"new_{random.randint(1, 99)}@mail.com", "new_pass12345", "New bio", "https://dicebear.com")])
    def test_user_info_changes(self, auth_user, main_page, settings_page, conduit_api, login_page,
                               username, email, password, bio, image):
        main_page.visit("/")

        with allure.step("Go to the Settings Page"):
            main_page.click_settings_button()
            expect(settings_page.page).to_have_url(re.compile(r".*/settings"))

        with allure.step("Change user info"):
            settings_page.change_user_info(username, email, password, bio, image)

        with allure.step("UI: verify changing"):
            expect(settings_page.page).not_to_have_url(re.compile(r".*/settings"))
            expect(settings_page.page).to_have_url(re.compile(r".*realworld.show.*"))

            expect(settings_page.page.locator(".navbar").locator(f"a[href*='/profile/{username}']")).to_be_visible()
            expect(main_page.page.locator("h4")).to_have_text(username)
            expect(main_page.page.locator("img.user-img")).to_have_attribute("src", image)

        with allure.step("API: verify changing"):
            response = conduit_api.users.get_current_user()

            assert response.json()["user"]["image"] == image
            assert response.json()["user"]["username"] == username
            assert response.json()["user"]["email"] == email
            assert response.json()["user"]["bio"] == bio

    @allure.title("Boundary Value Analysis: user info change fields")
    @pytest.mark.parametrize("username, email, is_valid", [
        # --- USERNAME LIMITS (Limit 60) ---
        ("", "valid1@mail.com", False),  # 0 (Error)
        ("U" * 60, "valid1@mail.com", True),  # 59 (Valid)
        ("u" * 61, "valid2@mail.com", False),  # 60 (Error)

        # --- EMAIL LIMITS (Limit 100) ---
        ("username", "", False),  # 0 (Error)
        ("username", ("a" * 91) + "@gmail.com", False),  # 100 (Error)
        ("username", ("A" * 90) + "@gmail.com", True)  # 99 (Valid)
    ])
    def test_validation_user_info_changes(self, auth_user, main_page, settings_page, username, email, is_valid):
        main_page.visit("/")

        with allure.step("Go to the Settings Page"):
            main_page.click_settings_button()
            expect(settings_page.page).to_have_url(re.compile(r".*/settings"))

        with allure.step("Change user info"):
            settings_page.change_user_info(username=username, email=email)

        if is_valid:
            with allure.step("Checking the redirect to the main page"):
                expect(settings_page.page).not_to_have_url(re.compile(r".*/settings"))
                expect(settings_page.page).to_have_url(re.compile(r".*realworld.show.*"))
        else:
            with allure.step("Checking if a validation error occurs"):
                settings_page.check_error_message("string of less than")

    @allure.title("Login with wrong password")
    def test_login_with_wrong_password(self, conduit_api, login_page):
        with allure.step("Create user"):
            user = generate_conduit_user()
            response = conduit_api.users.register_user(user)
            assert response.status_code == 201

        with allure.step("Login under created user with wrong password"):
            email = user["user"]["email"]
            password = user["user"]["password"] + "_wrong"

            login_page.visit("/login")
            login_page.login(email, password)

        with allure.step("Check error"):
            login_page.check_error_message("credentials invalid")

    @allure.title("Logout via UI")
    def test_logout(self, auth_user, conduit_api, settings_page, main_page):
        with allure.step("Logout from Setting page"):
            settings_page.visit(f"/settings")
            settings_page.logout()

        with allure.step("Verify of logout"):
            expect(main_page.page).not_to_have_url(re.compile(r".*/settings"))
            expect(main_page.page).to_have_url(re.compile(r".*realworld.show.*"))

            expect(main_page.login_link).to_be_visible()
            expect(main_page.register_link).to_be_visible()
            expect(main_page.new_post_link).not_to_be_visible()
