import requests

def test_contribute_page():
    response = requests.get("http://127.0.0.1:8080/contribute/")
    print(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    assert "Contribute" in response.text

test_contribute_page()