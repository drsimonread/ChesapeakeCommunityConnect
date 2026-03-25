import os
import requests

BASE_URL = "http://127.0.0.1:8080/DJadmin/"

def test_homepage():
    response = requests.get(BASE_URL + "/DJadmin/")
    assert response.status_code < 500
    assert "DJadmin" in response.text