import pytest
from weather_be import Weather
from open_api import OpenApi, ApiRequest, InvalidApiKey 
from unittest.mock import MagicMock, patch

mock_valid_response = {

	"location": {
		"name": "Tel Aviv-Yafo",
		"region": "Tel Aviv",
		"country": "Israel",
		"tz_id": "Asia/Jerusalem",
	},	"forecast": {
		"forecastday": [
			
				{"date": "2025-01-18",
				"day": {
						"maxtemp_c": 17.5, "mintemp_c": 13.4, "avgtemp_c": 15.7, "avghumidity": 62,
						}
            	},
			
				{"date": "2025-01-19",
				"day": {
					"maxtemp_c": 17.6, "mintemp_c": 14.5, "avgtemp_c": 15.8, "avghumidity": 59,
                    }
				}]
			}
		}


mock_invalid_input = {

			"error": {
				"code": 1006,
				"message": "No matching location found."
    				}
				}


@pytest.fixture()
def weather():

	mock_open_url = MagicMock(return_value=(mock_valid_response, 200))

	with patch('weather_be.Weather.call_api', mock_open_url):
		
		user_request = ApiRequest("Tel Aviv", 2)
		forecast_object = Weather(user_request)

	return forecast_object


@pytest.fixture()
def error_weather():

	mock_open_url = MagicMock(return_value=(mock_invalid_input, 400))

	with patch('weather_be.Weather.call_api', mock_open_url):

		user_request = ApiRequest("s", 3)
		forecast_object = Weather(user_request)
	
	return forecast_object





def test_init(weather):

	assert isinstance(weather.data, dict), "expected dict"
	assert weather.data["city"] == ["Tel Aviv-Yafo"], "expected Tel Aviv-Yafo element in city"
	assert weather.data["max_temp"][0] == 17.5, "expected 17.5"
	assert weather.data["max_temp"][1] == 17.6, "expected 17.6"

	assert weather.error == None, "expected None"

	assert isinstance(weather.error, type(None)), "expected type None"
	assert isinstance(weather.response, dict), "expected dict"
	assert len(weather.response["forecast"]["forecastday"]) == 2, "expected 2"

def test_invalid_input_init(error_weather):


	assert error_weather.error == "No matching location found.", "expected error messgae from json"
	
	assert error_weather.status_code == 400, f"expected 400 got {error_weather.status_code}"

	assert isinstance(error_weather.error, str), "expected str"
	assert isinstance(error_weather.response, dict), "expected dict"
	assert "error" in error_weather.response, "expected True"



