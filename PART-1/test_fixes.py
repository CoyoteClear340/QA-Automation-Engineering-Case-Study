import pytest
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

LOGIN_URL = "https://app.workflowpro.com/login"
DASHBOARD_URL = "https://app.workflowpro.com/dashboard"

def login(page, email, password):
    page.goto(LOGIN_URL)

    page.fill("#email", email)
    page.fill("#password", password)

    page.click("#login-btn")

    # --- Wait for navigation or dashboard UI to stabilize ---
    page.wait_for_url("**/dashboard*", timeout=15000)

    # --- Handle 2FA if it appears (sometimes only) ---
    twofa_input = page.locator("#twofa-code")

    if twofa_input.is_visible(timeout=2000):
        # In real automation you'd retrieve the code dynamically
        page.fill("#twofa-code", "123456")
        page.click("#twofa-submit")

        # Wait again for dashboard after 2FA
        page.wait_for_url("**/dashboard*", timeout=15000)

    # --- Wait for key dashboard element that indicates ready ---
    page.wait_for_selector(".welcome-message", timeout=15000)


def test_user_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login(page, "admin@company1.com", "password123")

        # Allow query params, not strict URL equality
        assert page.url.startswith(DASHBOARD_URL)

        # Case-insensitive check
        welcome_text = page.locator(".welcome-message").inner_text()
        assert "welcome" in welcome_text.lower()

        browser.close()


def test_multi_tenant_access():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login(page, "user@company2.com", "password123")

        # Tenant data may load slower — wait for project list
        page.wait_for_selector(".project-card", timeout=20000)

        projects = page.locator(".project-card")

        count = projects.count()
        assert count > 0, "Expected projects but found none"

        for i in range(count):
            text = projects.nth(i).inner_text()
            assert "company2" in text.lower()

        browser.close()
