import requests

ENDPOINT = "http://localhost:8000"

def test_pingable():
    health_url = ENDPOINT + "/health"
    response = requests.get(health_url)
    assert response.status_code == 200

