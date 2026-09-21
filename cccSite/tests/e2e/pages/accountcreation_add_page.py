from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tests.e2e.pages.base_page import BasePage

class AccountCreationAddPage(BasePage):
    EMAIL = (By.CSS_SELECTOR, "#id_email")
    USERNAME = (By.CSS_SELECTOR, "#id_username")
    DISPLAY = (By.CSS_SELECTOR, "#id_displayname")
    PASS = (By.CSS_SELECTOR, "#id_password")
    CONF = (By.CSS_SELECTOR, "#id_confirmpassword")
    STATUS = (By.CSS_SELECTOR, "#id_status")  # if visible
    SAVE = (By.CSS_SELECTOR, "input[name='_save']")

    def is_loaded(self):
        self.wait_for_visible(self.EMAIL); return True

    def create(self, email, username, display, password, status="pending"):
        self.type(self.EMAIL, email)
        self.type(self.USERNAME, username)
        self.type(self.DISPLAY, display)
        self.type(self.PASS, password)
        self.type(self.CONF, password)
        # If the form doesn’t expose status, comment this next line:
        Select(self.driver.find_element(*self.STATUS)).select_by_value(status)
        self.click(self.SAVE)
