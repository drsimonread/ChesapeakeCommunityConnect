import requests

def test_search_page_loads(base_url):
    response = requests.get(base_url + "/search/", timeout=5)
    assert response.status_code == 200
    assert "Chesapeake Community Connect - Forums" in response.text