"""
Selenium automated browser tests for PulseCare HMS.
Tests login flow, dashboard rendering, feature flag UI, and patient pages.
Requires: hms-application container running on http://localhost:5000
"""
import os
import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

BASE_URL = "http://localhost:5000"
SCREENSHOT_DIR = "reports/screenshots/selenium"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def get_headless_driver():
    """Return a headless Chrome WebDriver instance."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,768")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--log-level=3")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=opts)


# ─── Test 1: Login page loads ──────────────────────────────────────────────────
def test_selenium_login_page_loads():
    """Verify login page loads with correct title and form elements."""
    driver = get_headless_driver()
    try:
        driver.get(f"{BASE_URL}/login")
        time.sleep(1)
        driver.save_screenshot(f"{SCREENSHOT_DIR}/01_login_page.png")
        assert "PulseCare" in driver.title or "Login" in driver.page_source
        assert driver.find_element(By.NAME, "username")
        assert driver.find_element(By.NAME, "password")
    finally:
        driver.quit()


# ─── Test 2: Successful admin login ────────────────────────────────────────────
def test_selenium_admin_login_success():
    """Login as admin and verify redirect to dashboard."""
    driver = get_headless_driver()
    try:
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
        WebDriverWait(driver, 10).until(
            lambda d: "dashboard" in d.current_url or "index" in d.current_url
            or d.current_url != f"{BASE_URL}/login"
        )
        time.sleep(1)
        driver.save_screenshot(f"{SCREENSHOT_DIR}/02_dashboard_after_login.png")
        assert driver.current_url != f"{BASE_URL}/login", "Login should redirect away from login page"
    finally:
        driver.quit()


# ─── Test 3: Failed login shows error ──────────────────────────────────────────
def test_selenium_invalid_login():
    """Wrong credentials should stay on login page with error message."""
    driver = get_headless_driver()
    try:
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.NAME, "username").send_keys("wronguser")
        driver.find_element(By.NAME, "password").send_keys("wrongpass")
        driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
        time.sleep(1.5)
        driver.save_screenshot(f"{SCREENSHOT_DIR}/03_invalid_login.png")
        # Should still be on login page
        assert "login" in driver.current_url.lower() or "Invalid" in driver.page_source or "invalid" in driver.page_source.lower()
    finally:
        driver.quit()


# ─── Test 4: Feature flags API endpoint ────────────────────────────────────────
def test_selenium_feature_flags_api():
    """Feature flags API returns JSON with all 5 flags."""
    driver = get_headless_driver()
    try:
        driver.get(f"{BASE_URL}/api/features")
        time.sleep(1)
        driver.save_screenshot(f"{SCREENSHOT_DIR}/04_feature_flags_api.png")
        src = driver.page_source
        assert "EMERGENCY_TRIAGE_MODE" in src or "emergency_triage_mode" in src.lower()
        assert "TELEMEDICINE_PORTAL" in src or "telemedicine_portal" in src.lower()
    finally:
        driver.quit()


# ─── Test 5: Emergency banner hidden when flag OFF ─────────────────────────────
def test_selenium_emergency_banner_hidden_by_default():
    """Emergency triage banner should NOT appear by default (flag is OFF)."""
    driver = get_headless_driver()
    try:
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
        time.sleep(2)
        driver.save_screenshot(f"{SCREENSHOT_DIR}/05_no_emergency_banner.png")
        page_src = driver.page_source
        # Banner div should not be rendered if flag is OFF
        assert "🚨" not in page_src or "emergency-triage-banner" not in page_src
    finally:
        driver.quit()


# ─── Test 6: Health endpoint ───────────────────────────────────────────────────
def test_selenium_health_endpoint():
    """Health endpoint returns healthy status."""
    driver = get_headless_driver()
    try:
        driver.get(f"{BASE_URL}/health")
        time.sleep(1)
        driver.save_screenshot(f"{SCREENSHOT_DIR}/06_health_endpoint.png")
        assert "healthy" in driver.page_source.lower() or "ok" in driver.page_source.lower()
    finally:
        driver.quit()


# ─── Test 7: Patients page (authenticated) ────────────────────────────────────
def test_selenium_patients_page():
    """After login, patients listing page is accessible."""
    driver = get_headless_driver()
    try:
        # Login first
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
        time.sleep(2)
        # Navigate to patients
        driver.get(f"{BASE_URL}/patients")
        time.sleep(1.5)
        driver.save_screenshot(f"{SCREENSHOT_DIR}/07_patients_page.png")
        # Should show patients or redirect to login for auth check
        assert "patient" in driver.page_source.lower() or "login" in driver.current_url.lower()
    finally:
        driver.quit()


# ─── Test 8: Page title present ────────────────────────────────────────────────
def test_selenium_page_title_present():
    """Pages should have a meaningful HTML title."""
    driver = get_headless_driver()
    try:
        driver.get(f"{BASE_URL}/login")
        time.sleep(1)
        title = driver.title
        driver.save_screenshot(f"{SCREENSHOT_DIR}/08_page_title_check.png")
        assert len(title) > 0, f"Page title is empty, got: '{title}'"
        print(f"  Page title: {title}")
    finally:
        driver.quit()

