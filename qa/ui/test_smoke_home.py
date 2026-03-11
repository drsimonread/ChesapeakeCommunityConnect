import os
import requests

BASE_URL = os.getenv("QA_BASE_URL", "http://127.0.0.1:8080")

def test_homepage():
    r = requests.get(BASE_URL + "/", timeout=5)
    assert r.status_code == 200
