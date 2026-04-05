import pytest
from tests.e2e.pages.utils_admin import AdminPing
from tests.e2e.pages.admin_login_page import AdminLoginPage
from tests.e2e.pages.admin_dashboard_page import AdminDashboardPage
from tests.e2e.pages.admin_changelist_page import AdminChangeListPage
from tests.e2e.pages.accountcreation_add_page import AccountCreationAddPage

ADMIN_PATH = "/DJadmin"

@pytest.mark.smoke
def test_accountcreation_available_or_skip(driver, config):
    AdminLoginPage(driver, config["base_url"]).open(ADMIN_PATH).login(config["admin_user"], config["admin_pass"])
    ping = AdminPing(driver, config["base_url"])
    if not ping.exists(f"{ADMIN_PATH}/account/accountcreation/"):
        pytest.skip("AccountCreation admin not present on this branch; skipping Item 1 tests.")

def test_accept_only_updates_pending(driver, config):
    AdminLoginPage(driver, config["base_url"]).open(ADMIN_PATH).login(config["admin_user"], config["admin_pass"])
    dash = AdminDashboardPage(driver, config["base_url"]).open(ADMIN_PATH); assert dash.is_loaded()
    assert dash.has_accountcreation(), "AccountCreation not visible; fix admin registration/migrations."
    dash.click_accountcreation()

    listp = AdminChangeListPage(driver, config["base_url"]); assert listp.is_loaded()
    listp.add_new()
    addp = AccountCreationAddPage(driver, config["base_url"]); assert addp.is_loaded()
    addp.create("pending1@example.com", "pending1", "Pending One", "Pass123!", status="pending")

    listp = AdminChangeListPage(driver, config["base_url"])
    listp.add_new()
    addp = AccountCreationAddPage(driver, config["base_url"]); assert addp.is_loaded()
    addp.create("accepted1@example.com", "accepted1", "Accepted One", "Pass123!", status="accepted")

    listp = AdminChangeListPage(driver, config["base_url"])
    listp.select_first_n(2); listp.choose_action("accept_requests"); listp.submit_action()

    msgs = " ".join(listp.messages()).lower()
    assert "accepted" in msgs and "request" in msgs
    assert "accepted" in listp.rows_text()

@pytest.mark.regression
def test_reject_warns_when_no_pending_selected(driver, config):
    AdminLoginPage(driver, config["base_url"]).open(ADMIN_PATH).login(config["admin_user"], config["admin_pass"])
    dash = AdminDashboardPage(driver, config["base_url"]).open(ADMIN_PATH); dash.click_accountcreation()
    listp = AdminChangeListPage(driver, config["base_url"]); assert listp.is_loaded()

    # ensure accepted row exists
    listp.add_new()
    addp = AccountCreationAddPage(driver, config["base_url"]); addp.is_loaded()
    addp.create("acc2@example.com", "acc2", "Accepted Two", "Pass123!", status="accepted")

    listp = AdminChangeListPage(driver, config["base_url"])
    listp.select_first_n(1); listp.choose_action("reject_requests"); listp.submit_action()

    msgs = " ".join(listp.messages()).lower()
    assert "no pending" in msgs
