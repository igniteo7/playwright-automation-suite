"""
TEST SUITE: Login — Playwright version

Key Playwright concepts demonstrated here:
  - page.expect_navigation() for waiting on URL changes
  - Parameterised tests with pytest.mark.parametrize
  - Assertions using Playwright's expect() for auto-retry
"""

import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from fixtures.mock_data import INVALID_USERS, VALID_USER


class TestLogin:

    def test_valid_login_reaches_inventory(self, page):
        login = LoginPage(page).open()
        login.login(VALID_USER["username"], VALID_USER["password"])
        # expect() auto-retries until the condition is true or timeout is reached
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    def test_page_title(self, page):
        LoginPage(page).open()
        expect(page).to_have_title("Swag Labs")

    def test_login_button_is_visible(self, page):
        LoginPage(page).open()
        expect(page.locator("#login-button")).to_be_visible()

    @pytest.mark.parametrize("username,password,expected_error", INVALID_USERS)
    def test_invalid_login_shows_error(self, page, username, password, expected_error):
        """
        Parameterised: runs once per tuple in INVALID_USERS.
        Each run gets a fresh page (function-scoped fixture default).
        """
        login = LoginPage(page).open()
        login.login(username, password)
        error = login.get_error_message()
        assert error is not None, f"Expected error for user='{username}'"
        assert expected_error.lower() in error.lower(), (
            f"Expected '{expected_error}' in error message, got: '{error}'"
        )

    def test_error_message_can_be_dismissed(self, page):
        """The ✕ button on the error banner should clear the message."""
        login = LoginPage(page).open()
        login.login("bad_user", "bad_pass")
        close_btn = page.locator(".error-button")
        close_btn.click()
        expect(page.locator("[data-test='error']")).not_to_be_visible()
