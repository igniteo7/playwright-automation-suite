"""
PAGE OBJECT MODEL — LoginPage (Playwright version)

Playwright locators are "lazy" — they don't search the DOM until you act on them.
This means they automatically wait for the element to appear (up to the timeout).
No need for explicit WebDriverWait like in Selenium.
"""


class LoginPage:
    def __init__(self, page):
        self.page = page
        # Playwright locators — these don't query the DOM until you call an action
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button   = page.locator("#login-button")
        self.error_message  = page.locator("[data-test='error']")

    def open(self):
        self.page.goto("https://www.saucedemo.com")
        return self

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def get_error_message(self) -> str | None:
        if self.error_message.is_visible():
            return self.error_message.text_content()
        return None

    def is_logged_in(self) -> bool:
        return "/inventory" in self.page.url
