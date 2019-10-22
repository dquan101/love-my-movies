import requests


def test_get():
    try:
        r = requests.get('http://localhost:5000').status_code
    except:
        r = 500
    assert r == 200

test_get()