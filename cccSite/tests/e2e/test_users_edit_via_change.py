import pytest
from selenium.webdriver.common.by import By
from tests.e2e.pages.admin_login_page import AdminLoginPage
from tests.e2e.pages.admin_changelist_page import AdminChangeListPage
from tests.e2e.pages.user_add_edit_page import UserAddEditPage

ADMIN_PATH = "/DJadmin"

@pytest.mark.regression
def test_users_edit_by_opening_row(driver, config):
    AdminLoginPage(driver, config["base_url"]).open(ADMIN_PATH).login(config["admin_user"], config["admin_pass"])
    listp = AdminChangeListPage(driver, config["base_url"]).open(f"{ADMIN_PATH}/auth/user/"); assert listp.is_loaded()

    # Open first row's change form (first link in first column)
    first_link = driver.find_element(By.CSS_SELECTOR, "#result_list tbody tr th a")
    first_link_text = first_link.text
    first_link.click()

    form = UserAddEditPage(driver, config["base_url"]); assert form.is_loaded()
    form.set_fields(email="updated@example.com", first="QA", last="Check")

    # back on list, confirm edited row shows updated email or name
    assert "updated@example.com" in listp.rows_text() or "QA" in listp.rows_text()
