# tests/e2e/test_landing_page.py
import pytest
from tests.e2e.pages.landing_page import LandingPage  # absolute import

@pytest.mark.smoke
def test_landing_page_loads(driver, config):
    page = LandingPage(driver, config["base_url"]).go()
    assert page.is_loaded(), "Landing page did not load correctly"
    # Loosely assert some expected text on your landing page; tweak to something real
    assert "Welcome" in driver.page_source or "Community" in driver.page_source

