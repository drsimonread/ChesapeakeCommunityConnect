import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8080/").rstrip("/")

def test_homepage():
    r = requests.get(f"{BASE_URL}/", timeout=5)

    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    expected_text = "Chesapeake Community Connect"
    assert expected_text in r.text, f"Could not find'{expected_text}' in homepage html"

    if __name__ == "__main__":
        test_homepage()
        print("Homepage test passed!")