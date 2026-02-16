import os
import requests

def test_homepage_responds():
    base_url = os.getenv("QA_BASE_URL", "http://127.0.0.1:8080")
    r = requests.get(base_url + "/", timeout=5)
    assert r.status_code < 500

