import os
import requests

BASE_URL = "http://127.0.0.1:8080"

def test_homepage():
    response = requests.get(BASE_URL + "/smoke test/")
    assert response.status_code == 200
    assert "Smoke Test" in response.text
