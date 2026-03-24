"""
PAGE OBJECT MODEL — InventoryPage (Playwright version)
"""


class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.product_names  = page.locator(".inventory_item_name")
        self.product_prices = page.locator(".inventory_item_price")
        self.sort_dropdown  = page.locator(".product_sort_container")
        self.cart_badge     = page.locator(".shopping_cart_badge")
        self.cart_link      = page.locator(".shopping_cart_link")

    def get_product_names(self) -> list[str]:
        return self.product_names.all_text_contents()

    def get_product_prices(self) -> list[float]:
        texts = self.product_prices.all_text_contents()
        return [float(t.replace("$", "")) for t in texts]

    def add_item_by_name(self, product_name: str):
        """
        Adds a specific product by name. Uses Playwright's has_text filter
        to find the right item — a clean alternative to brittle index-based selectors.
        """
        item = self.page.locator(".inventory_item", has_text=product_name)
        item.locator("[data-test^='add-to-cart']").click()
        return self

    def add_first_item(self):
        self.page.locator("[data-test^='add-to-cart']").first.click()
        return self

    def sort_by(self, value: str):
        """
        value options: 'az', 'za', 'lohi', 'hilo'
        """
        self.sort_dropdown.select_option(value)
        return self

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    def go_to_cart(self):
        self.cart_link.click()
