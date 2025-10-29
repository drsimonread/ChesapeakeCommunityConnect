from selenium.webdriver.common.by import By
from tests.e2e.pages.base_page import BasePage

class UserAddEditPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, "#id_username")
    EMAIL = (By.CSS_SELECTOR, "#id_email")
    FIRST = (By.CSS_SELECTOR, "#id_first_name")
    LAST = (By.CSS_SELECTOR, "#id_last_name")
    SAVE = (By.CSS_SELECTOR, "input[name='_save']")

    def is_loaded(self):
        self.wait_for_visible(self.USERNAME); return True

    def set_fields(self, username=None, email=None, first=None, last=None):
        if email is not None: self.type(self.EMAIL, email)
        if first is not None: self.type(self.FIRST, first)
        if last is not None: self.type(self.LAST, last)
        self.click(self.SAVE)
