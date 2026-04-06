import requests

# list of URLs to smoke test
urls = [
    "http://127.0.0.1:8000/cdspec/",
    "http://127.0.0.1:8000/about/"
]

def test_page(url):
    # sends a GET request to the URL
    response = requests.get(url)

    # prints the URL being tested and its status code
    print(f"\nTesting: {url}")
    print(f"Response status code: {response.status_code}")

    # if statement: checks if the status code is 500 (server error) and prints the result
    if response.status_code == 500:
        print(f"FAILED — got 500 Server Error")
    else:
        print(f"PASSED")

# for loop: loops through all URLs and test each one
for url in urls:
    test_page(url)