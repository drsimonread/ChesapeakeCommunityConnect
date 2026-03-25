import requests

BASE_URL = "http://127.0.0.1:8080/"

def test_homepage():
    response = requests.get(BASE_URL + "/homepage/")
    assert response.status_code == 200
    assert "Chesapeake Community Connect" in response.text

    