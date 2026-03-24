"""
CONFTEST — Playwright Project

pytest-playwright automatically provides 'browser', 'context', and 'page' fixtures.
Here we extend them with:
  - A logged-in page fixture
  - Shared base URL
  - Slow-mo option for debugging
"""

import pytest

BASE_URL = "https://www.saucedemo.com"


def pytest_addoption(parser):
    """Add a --slowmo flag so you can watch the browser during debugging."""
    parser.addoption("--slowmo", action="store", default=0, type=int,
                     help="Slow down Playwright actions by N milliseconds")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig):
    """
    Session-scoped: applies to all tests.
    Sets viewport size for consistent rendering.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture
def logged_in_page(page):
    """
    Gives you a Playwright page already authenticated.
    Re-used by tests that don't need to test the login flow itself.
    """
    page.goto(BASE_URL)
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")
    return page
