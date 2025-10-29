from selenium.webdriver.common.by import By
from tests.e2e.pages.base_page import BasePage

class AdminLoginPage(BasePage):
    USER = (By.CSS_SELECTOR, "#id_username, input[name='username']")
    PASS = (By.CSS_SELECTOR, "#id_password, input[name='password']")
    SUBMIT = (By.CSS_SELECTOR, "form [type='submit']")
    FORM = (By.CSS_SELECTOR, "form")

    def open(self, admin_base):
        return super().open(f"{admin_base}/login/")

    def is_loaded(self):
        self.wait_for_visible(self.FORM); return True

    def login(self, username, password):
        self.type(self.USER, username)
        self.type(self.PASS, password)
        self.click(self.SUBMIT)
