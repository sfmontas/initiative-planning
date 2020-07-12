from os import getenv
import requests

def test_post_headers_body_json():
    url = getenv("API_URL") or 'http://localhost:8000/'
    url += "break"
    # Additional headers.
    headers = {'Content-Type': 'application/json' }

    # Body
    # convert dict to json by json.dumps() for body data.
    resp = requests.get(url)
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['message'] == "Hello World!"
