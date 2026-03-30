import requests

def test_djadmin_home_responds(base_url):
    response = requests.get(base_url + "/DJadmin/", timeout=5)
    assert response.status_code < 500