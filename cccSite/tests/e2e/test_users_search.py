import pytest
from tests.e2e.pages.admin_login_page import AdminLoginPage
from tests.e2e.pages.admin_changelist_page import AdminChangeListPage

ADMIN_PATH = "/DJadmin"

@pytest.mark.smoke
def test_users_search(driver, config):
    AdminLoginPage(driver, config["base_url"]).open(ADMIN_PATH).login(config["admin_user"], config["admin_pass"])

    listp = AdminChangeListPage(driver, config["base_url"]).open(f"{ADMIN_PATH}/auth/user/")
    assert listp.is_loaded()

    listp.search("admin")   # replace with a username you know exists
    assert "admin" in listp.rows_text()
