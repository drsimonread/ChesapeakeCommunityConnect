import requests

BASE_URL = "http://127.0.0.1:8080"

def test_help_page_loads():
    response = requests.get(BASE_URL + "/help/")
    assert response.status_code == 200
    assert "Help" in response.text