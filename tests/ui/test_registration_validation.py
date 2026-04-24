import re

import allure
import pytest
from playwright.sync_api import expect


@pytest.mark.ui
@allure.feature("UI: Registration Page")
@allure.story("Validation of the Registration form")
class TestRegistrationValidation:

    @allure.title("Registration with empty fields")
    @pytest.mark.parametrize("username, email, password", [
        ("", "test@mail.com", "password123"),
        ("username", "test@mail.com", ""),
        ("username", "", "password123"),
        ("", "", "")
    ])
    def test_register_empty_fields_validation(self, register_page, username, email, password):
        register_page.visit("/register")
        register_page.registration(username, email, password)
        register_page.register_button_disabled()

    @allure.title("Boundary Value Analysis: Registration fields")
    @pytest.mark.parametrize("username, email, password, is_valid", [
        # --- USERNAME LIMITS (Limit 60) ---
        ("U" * 60, "valid1@mail.com", "pass12345", True),  # 59 (Valid)
        ("u" * 61, "valid2@mail.com", "pass12345", False),  # 60 (Error)

        # --- EMAIL LIMITS (Limit 100) ---
        ("user1", ("A" * 90) + "@gmail.com", "pass12345", True),  # 99 (Valid)
        ("user2", ("a" * 91) + "@gmail.com", "pass12345", False),  # 100 (Error)

        # --- PASSWORD LIMITS (Limit 60) ---
        ("user3", "valid3@mail.com", "P" * 60, True),  # 59 (Valid)
        ("user4", "valid4@mail.com", "p" * 61, False)  # 60 (Error)
    ])
    def test_register_boundary_values(self, register_page, username, email, password, is_valid):
        register_page.visit("/register")

        with allure.step(f"Registration: Username({len(username)}), Email({len(email)}), Pass({len(password)})"):
            register_page.registration(username, email, password)

        if is_valid:
            with allure.step("Checking the redirect to the main page"):
                expect(register_page.page).not_to_have_url(re.compile(r".*/register"))
                expect(register_page.page).to_have_url(re.compile(r".*realworld.show.*"))
        else:
            with allure.step("Checking if a validation error occurs"):
                register_page.check_error_message("length less than")
