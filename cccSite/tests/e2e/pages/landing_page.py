# tests/e2e/pages/landing_page.py
from selenium.webdriver.common.by import By
from tests.e2e.pages.base_page import BasePage  # absolute import

class LandingPage(BasePage):
    # Adjust this selector to something that exists on your homepage (hero/banner/main)
    BODY = (By.TAG_NAME, "body")

    def go(self):
        # navigate to homepage
        return super().open("/")

    def is_loaded(self):
        self.wait_for_visible(self.BODY)
        return True

