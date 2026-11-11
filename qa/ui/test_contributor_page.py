import requests

def test_contributor_page_loads(base_url):
    response = requests.get(base_url + "/account/view/contributor/", timeout=5)
    assert response.status_code == 200
    assert "What it means to be a Contributor" in response.text