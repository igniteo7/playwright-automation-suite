"""
TEST SUITE: Cart & Network Interception — Playwright's killer feature

Network interception (page.route) lets you:
  1. Mock API responses — test UI behavior without a live backend
  2. Block requests — simulate slow networks or outages
  3. Assert which requests were made — verify the frontend calls the right endpoints

This is one of the things that makes Playwright much more powerful than Selenium
for modern web apps.
"""

import pytest
from playwright.sync_api import expect, Page
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from fixtures.mock_data import VALID_USER, PRODUCTS


class TestCartFlow:

    def test_add_item_updates_badge(self, logged_in_page: Page):
        """Adding one item should show badge count = 1."""
        inv = InventoryPage(logged_in_page)
        inv.add_first_item()
        assert inv.get_cart_count() == 1

    def test_add_specific_item_by_name(self, logged_in_page: Page):
        """We should be able to target a product by name, not just position."""
        inv = InventoryPage(logged_in_page)
        inv.add_item_by_name("Sauce Labs Backpack")
        assert inv.get_cart_count() == 1

    def test_cart_persists_after_navigation(self, logged_in_page: Page):
        """
        Items in the cart should still be there after navigating away and back.
        This tests session/state persistence — a common regression in SPAs.
        """
        inv = InventoryPage(logged_in_page)
        inv.add_first_item()

        # Navigate away
        logged_in_page.goto("https://www.saucedemo.com/about.html", wait_until="domcontentloaded")
        logged_in_page.go_back()

        # Badge should still show 1
        inv2 = InventoryPage(logged_in_page)
        assert inv2.get_cart_count() == 1, "Cart count should persist after navigating away"

    @pytest.mark.parametrize("product_name", PRODUCTS)
    def test_each_product_can_be_added(self, logged_in_page: Page, product_name: str):
        """Every product in our list should be individually addable to cart."""
        inv = InventoryPage(logged_in_page)
        inv.add_item_by_name(product_name)
        assert inv.get_cart_count() == 1, f"Failed to add '{product_name}' to cart"
        # Remove it again so the next parametrize iteration starts clean
        logged_in_page.locator("[data-test^='remove']").first.click()


class TestNetworkInterception:
    """
    Demonstrates Playwright's route interception — mocking API responses
    so the UI can be tested independently of the backend.
    """

    def test_intercept_and_mock_response(self, page: Page):
        """
        Intercept any request to a 'products' endpoint and return fake data.
        This proves the UI renders whatever the API returns — useful when
        the real API is unavailable or returns inconsistent test data.
        """
        # Set up the route BEFORE navigating — order matters
        def mock_handler(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"products": [{"id": 1, "name": "Mock Product", "price": 9.99}]}'
            )

        # Intercept requests matching this URL pattern
        page.route("**/api/products**", mock_handler)

        # Navigate (the real site doesn't call /api/products, but this
        # demonstrates the pattern you'd use on a real app)
        page.goto("https://www.saucedemo.com")
        # In a real app with an API, you'd now assert the mocked data appears in the UI

    def test_block_image_requests(self, page: Page):
        """
        Block all image requests. Useful for:
        - Speeding up tests (images are slow to load)
        - Testing layout without images (content-first rendering)
        """
        page.route("**/*.{png,jpg,jpeg,gif,svg,webp}", lambda route: route.abort())

        login = LoginPage(page).open()
        login.login(VALID_USER["username"], VALID_USER["password"])

        # Page should still load and be functional even without images
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        inv = InventoryPage(page)
        names = inv.get_product_names()
        assert len(names) > 0, "Products should still list even with images blocked"

    def test_capture_network_requests(self, page: Page):
        """
        Listen to all network requests made during login.
        Useful for verifying the correct endpoints are called.
        """
        captured_requests = []

        page.on("request", lambda req: captured_requests.append(req.url))

        login = LoginPage(page).open()
        login.login(VALID_USER["username"], VALID_USER["password"])
        page.wait_for_url("**/inventory.html")

        # At minimum the main page and inventory should have been loaded
        assert any("saucedemo.com" in url for url in captured_requests), (
            "Expected at least one request to saucedemo.com"
        )
