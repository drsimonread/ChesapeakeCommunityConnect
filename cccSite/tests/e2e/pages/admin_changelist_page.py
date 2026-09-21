from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tests.e2e.pages.base_page import BasePage

class AdminChangeListPage(BasePage):
    RESULT_TABLE = (By.CSS_SELECTOR, "#result_list")
    ADDLINK = (By.CSS_SELECTOR, ".object-tools a.addlink, a.addlink")
    SEARCHBOX = (By.CSS_SELECTOR, "#searchbar, input[name='q']")
    SEARCHSUBMIT = (By.CSS_SELECTOR, "form[role='search'] [type='submit'], input[type='submit'][value='Search']")
    FILTER_SIDEBAR = (By.CSS_SELECTOR, "#changelist-filter, .filter-wrapper")
    ACTION_CHECKBOXES = (By.CSS_SELECTOR, "input.action-select[name='_selected_action']")
    ACTION_SELECT = (By.CSS_SELECTOR, "select[name='action']")
    ACTION_GO = (By.CSS_SELECTOR, ".actions [type='submit']")
    MESSAGES = (By.CSS_SELECTOR, "ul.messagelist li")
    ROWS = (By.CSS_SELECTOR, "#result_list tbody tr")

    def is_loaded(self):
        self.wait_for_visible(self.RESULT_TABLE); return True

    def add_new(self): self.click(self.ADDLINK)
    def search(self, text):
        self.type(self.SEARCHBOX, text); self.click(self.SEARCHSUBMIT)
    def select_first_n(self, n=1):
        for b in self.driver.find_elements(*self.ACTION_CHECKBOXES)[:n]: b.click()
    def choose_action(self, value):
        Select(self.driver.find_element(*self.ACTION_SELECT)).select_by_value(value)
    def submit_action(self): self.click(self.ACTION_GO)
    def messages(self): return [m.text.strip() for m in self.driver.find_elements(*self.MESSAGES)]
    def rows_text(self): return " ".join(r.text for r in self.driver.find_elements(*self.ROWS)).lower()
