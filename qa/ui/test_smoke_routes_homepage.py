import os
import requests

BASE_URL = os.getenv("APP_URL", "http://127.0.0.1:8080/")

def test_homepage():
    response = requests.get(f"{BASE_URL}/", timeout=10)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    expected_text = "Chesapeake Community Connect"
    assert expected_text in response.text, f"Expected text '{expected_text}' not found in homepage"

    if __name__ == "__main__":
        try:
            test_homepage()
            print("Homepage smoke test passed!")
        except AssertionError as e:
            print(f"Homepage smoke test failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")