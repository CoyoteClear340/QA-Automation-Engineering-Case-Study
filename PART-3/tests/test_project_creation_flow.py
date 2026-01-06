import requests
import pytest
from playwright.sync_api import sync_playwright
from selenium import webdriver


BASE_URL = "https://app.workflowpro.com"
API_URL = f"{BASE_URL}/api/v1/projects"

PROJECT_NAME = "Test Project 101"
TENANT_ID = "company1"
OTHER_TENANT_ID = "company2"


def create_project_api(token):
    # Payload used to create the project through backend API
    payload = {
        "name": PROJECT_NAME,
        "description": "Project created via API",
        "team_members": []
    }

    # Authorization and tenant routing information
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": TENANT_ID
    }

    # API call to create project
    res = requests.post(API_URL, json=payload, headers=headers)

    # Fail immediately if API does not return 2xx
    res.raise_for_status()

    # Return project id for later validation
    return res.json()["id"]


def test_project_full_flow():
   
    # 1. API: Create project
    token = "demo-api-token"   # In real-world tests, token would come from secure storage
    project_id = create_project_api(token)

    # 2. WEB UI: Verify project is visible to correct tenant users
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Login flow (assuming valid test credentials)
        page.goto(f"{BASE_URL}/login")
        page.fill("#email", "admin@company1.com")
        page.fill("#password", "password123")
        page.click("#login-btn")

        # Wait for dashboard elements to be available
        page.wait_for_selector(".project-card")

        # Validate created project appears in UI list
        assert PROJECT_NAME.lower() in page.content().lower()

        browser.close()

    # 3. MOBILE (BrowserStack): Validate project is also visible on mobile
    caps = {
        "platformName": "Android",
        "deviceName": "Google Pixel 7",
        "browserName": "chrome",
        "bstack:options": {
            "projectName": "WorkflowPro",
            "buildName": "Mobile Check"
        }
    }

    # Remote WebDriver session for BrowserStack
    driver = webdriver.Remote(
        command_executor="https://hub.browserstack.com/wd/hub",
        options=webdriver.ChromeOptions(),
    )
    driver.start_session(caps)

    # Login on mobile web view
    driver.get(f"{BASE_URL}/login")
    driver.find_element("id", "email").send_keys("admin@company1.com")
    driver.find_element("id", "password").send_keys("password123")
    driver.find_element("id", "login-btn").click()

    # Validate that created project is visible on mobile
    assert PROJECT_NAME.lower() in driver.page_source.lower()

    driver.quit()

    # 4. TENANT ISOLATION: Ensure project is NOT visible to another company
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": OTHER_TENANT_ID
    }

    # Fetch projects for another tenant
    res = requests.get(API_URL, headers=headers)
    res.raise_for_status()

    projects = [p["name"].lower() for p in res.json()]

    # Security check: project should not leak across tenants
    assert PROJECT_NAME.lower() not in projects
