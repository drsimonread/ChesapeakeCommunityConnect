import requests

def test_help_page_loads(base_url):
    response = requests.get(base_url + "/help/", timeout=5)
    assert response.status_code == 200
    assert "Help" in response.text