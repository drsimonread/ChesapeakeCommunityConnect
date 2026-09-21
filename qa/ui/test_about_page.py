import requests

def test_about_page_loads(base_url):
    response = requests.get(base_url + "/about/", timeout=5)
    assert response.status_code == 200
    assert "About" in response.text