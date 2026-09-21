# tests/e2e/pages/utils_admin.py
from selenium.webdriver.common.by import By
from tests.e2e.pages.base_page import BasePage

class AdminPing(BasePage):
    """Small helper to test if an admin changelist exists (returns True/False)."""
    def exists(self, absolute_or_relative_path: str, timeout: float = 5.0) -> bool:
        # absolute_or_relative_path example: "/DJadmin/account/accountcreation/"
        try:
            if absolute_or_relative_path.startswith("http"):
                url = absolute_or_relative_path
            else:
                # BasePage.open handles joining base_url + relative path
                url = absolute_or_relative_path
            self.open(url)
            # A valid admin page should have #content; change if your theme differs
            self.wait_for_visible((By.CSS_SELECTOR, "#content"), timeout=timeout)
            return True
        except Exception:
            return False

