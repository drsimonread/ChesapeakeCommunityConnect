import requests


def test_contribute_page():
    response = requests.get("http://127.0.0.1/contribute/")
    assert response.status_code == 200
    assert "Contribute" in response.text
