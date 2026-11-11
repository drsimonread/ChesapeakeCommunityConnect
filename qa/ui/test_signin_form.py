import requests 
def test_signin_form_loads(base_url):
    response = requets.get(base_url + "/account/signin-form/" , timeout=5)
    assert response.status_code == 200
    assert"Password:" in response.text