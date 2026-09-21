# tests/e2e/pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10

class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self, path=""):
        self.driver.get(self.base_url.rstrip("/") + "/" + path.lstrip("/"))
        return self

    def wait_for_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait_for_visible(locator)
        self.driver.find_element(*locator).click()

    def type(self, locator, text):
        self.wait_for_visible(locator)
        el = self.driver.find_element(*locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        self.wait_for_visible(locator)
        return self.driver.find_element(*locator).text

