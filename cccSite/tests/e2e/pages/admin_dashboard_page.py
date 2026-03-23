from selenium.webdriver.common.by import By
from tests.e2e.pages.base_page import BasePage

class AdminDashboardPage(BasePage):
    HEADER = (By.CSS_SELECTOR, "h1#site-name a")
    ACCOUNT_APP = (By.CSS_SELECTOR, ".app-account.module")
    ACCOUNT_MEMBER_ROW = (By.CSS_SELECTOR, ".app-account .model-member")
    ACCOUNT_CREATION_ROW = (By.CSS_SELECTOR, ".app-account .model-accountcreation")
    ACCOUNT_CREATION_LINK = (By.CSS_SELECTOR, ".app-account .model-accountcreation th a")

    MAP_APP = (By.CSS_SELECTOR, ".app-mapViewer.module")
    MAP_POST_ROW = (By.CSS_SELECTOR, ".app-mapViewer .model-post")
    MAP_POST_LINK = (By.CSS_SELECTOR, ".app-mapViewer .model-post th a")

    def open(self, admin_base):
        return super().open(f"{admin_base}/")

    def is_loaded(self):
        self.wait_for_visible(self.HEADER); return True

    def has_accountcreation(self):
        return len(self.driver.find_elements(*self.ACCOUNT_CREATION_ROW)) > 0

    def click_accountcreation(self):
        self.click(self.ACCOUNT_CREATION_LINK)

    def click_mappost(self):
        self.click(self.MAP_POST_LINK)
