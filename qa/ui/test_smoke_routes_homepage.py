import os
import requests

BASE_URL = "http://127.0.0.1:8080/"

def test_homepage():
    response = requests.get(BASE_URL + "/homepage/")

    assert response.status_code == 200
    expected_text = "Chesapeake Community Connect"
    assert expected_text in response.text

    if __name__ == "__main__":
        try:
            test_homepage()
            print("Homepage smoke test passed!")
        except AssertionError as e:
            print(f"Homepage smoke test failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")