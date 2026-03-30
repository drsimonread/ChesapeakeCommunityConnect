import requests

def test_homepage_loads(base_url):
    response = requests.get(base_url + "/", timeout=5)
    assert response.status_code == 200
    assert "Chesapeake Community Connect" in response.text