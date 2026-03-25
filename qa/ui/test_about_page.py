# import requests library to send HTTP requests
import requests

# define the base URL for the local server
BASE_URL = "http://127.0.0.1:8080"

# test to verify the About page loads correctly
def test_about_page_loads():

    # send a GET request to the /about/ page
    response = requests.get(BASE_URL + "/about/")

    # check that the response status code is 200 (OK)
    assert response.status_code == 200

    # check that the page contains the word "About"
    assert "About" in response.text