
import requests

def test_web_reachable():

	url = ("http://127.0.0.1:5000")
	response = requests.get(url)

	assert response.status_code == 200, f"expected 200. got {response.status_code}"


