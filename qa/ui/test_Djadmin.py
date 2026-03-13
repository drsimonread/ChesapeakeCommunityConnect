import os
import requests

BASE_URL = os.getenv("DJadmin", "http://127.0.0.1:8080/DJadmin/").rstrip("/")

def test_homepage():
    r = requests.get(f"{BASE_URL}/", timeout=5)
    assert r.status_code < 500, f"server returned a 500-level error: {r.status_code}"
    print(f"Status code: {r.status_code}")

if __name__ == "__main__":
    test_homepage()