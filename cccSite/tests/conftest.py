import os, pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def pytest_configure(config):
    print("Loaded tests/conftest.py")

@pytest.fixture(scope="session")
def config():
    load_dotenv(override=True)
    return {
        "base_url": os.getenv("BASE_URL", "http://127.0.0.1:8080"),
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "admin_user": os.getenv("CCC_ADMIN_USER", ""),
        "admin_pass": os.getenv("CCC_ADMIN_PASS", ""),
    }

@pytest.fixture
def driver(config):
    opts = Options()
    if config["headless"]:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
