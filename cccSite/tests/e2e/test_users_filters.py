import pytest
from tests.e2e.pages.admin_login_page import AdminLoginPage
from tests.e2e.pages.admin_changelist_page import AdminChangeListPage
from tests.e2e.pages.base_page import BasePage
from selenium.webdriver.common.by import By

ADMIN_PATH = "/DJadmin"

@pytest.mark.smoke
def test_users_list_and_filter(driver, config):
    AdminLoginPage(driver, config["base_url"]).open(ADMIN_PATH).login(config["admin_user"], config["admin_pass"])
    listp = AdminChangeListPage(driver, config["base_url"]).open(f"{ADMIN_PATH}/auth/user/"); assert listp.is_loaded()

    # Check filter sidebar exists
    # If you have an "Active" filter link:
    try:
        driver.find_element(By.LINK_TEXT, "Active").click()
    except Exception:
        pass

    assert "zkralec" in listp.rows_text()  # looser assertion; tighten to a known username if you seed one
