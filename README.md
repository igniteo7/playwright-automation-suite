# End-to-End Playwright Automation Suite

A cross-browser automated test suite built with **Python** and **Playwright**, targeting a React single-page application. Demonstrates advanced Playwright features including network interception, API mocking, route blocking, reusable fixtures, and CI integration via GitHub Actions.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Core language |
| Playwright | Cross-browser automation |
| pytest-playwright | Playwright-pytest integration |
| Pytest | Test runner & fixtures |
| GitHub Actions | CI/CD pipeline |

---

## Project Structure

```
project4/
├── pages/                    # Page Object Model classes
│   ├── login_page.py         # Login page
│   └── inventory_page.py     # Product listing page
├── tests/
│   ├── test_login.py         # Login flows + parametrised invalid cases
│   └── test_cart_flow.py     # Cart flows + network interception
├── fixtures/
│   └── mock_data.py          # Shared test data (users, product names)
├── conftest.py               # Playwright fixtures (logged-in page, viewport)
├── pytest.ini                # Pytest + Playwright config
└── requirements.txt
```

---

## Key Concepts Demonstrated

### Playwright vs Selenium
Playwright locators are **auto-waiting** — no manual `WebDriverWait` or `sleep()` needed. When you call `.click()`, Playwright waits for the element to be visible, stable, and enabled before acting.

```python
# Selenium — manual wait required
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

# Playwright — just click, it handles the wait
page.locator("#login-button").click()
```

### Network Interception & API Mocking
Playwright can intercept HTTP requests mid-flight and return mocked responses — allowing the UI to be tested independently of the backend.

```python
def mock_handler(route):
    route.fulfill(status=200, body='{"products": [...]}')

page.route("**/api/products**", mock_handler)
```

### Request Blocking
Block image or analytics requests to speed up test runs or simulate degraded conditions.

```python
page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
```

### Reusable Fixtures
The `logged_in_page` fixture in `conftest.py` handles authentication once and hands tests a ready-to-use page — avoiding repetitive login code across every test.

### Cross-Browser
Run the same suite against Chromium, Firefox, or WebKit with a single flag change:

```bash
pytest --browser firefox
pytest --browser webkit
```

---

## Setup & Run

```bash
# 1. Clone and enter the project
git clone https://github.com/YOUR_USERNAME/playwright-automation-suite
cd playwright-automation-suite

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers (one-time setup)
playwright install

# 5. Run all tests (headed — browser window opens)
pytest

# 6. Run headless (for CI or faster local runs)
pytest --headed=false

# 7. Run on a specific browser
pytest --browser firefox

# 8. Slow down execution for debugging
pytest --slowmo 800

# 9. Run a specific test file
pytest tests/test_cart_flow.py
```

---

## CI/CD

GitHub Actions runs the full suite headlessly on every push and pull request. See `.github/workflows/tests.yml`.

---

## Why These Tests Matter

| Test | What It Catches |
|------|----------------|
| `test_cart_persists_after_navigation` | Session/state bugs in SPAs |
| `test_each_product_can_be_added` | Per-item regression on product catalogue changes |
| `test_block_image_requests` | Layout breaks when assets fail to load |
| `test_capture_network_requests` | Frontend calling wrong endpoints after refactor |
| `test_error_message_can_be_dismissed` | UI state management bugs |
# playwright-automation-suite
