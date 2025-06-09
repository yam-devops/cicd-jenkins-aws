from typing import Union
from open_api import OpenApi, ApiRequest, InvalidApiKey 
from parser import Forecast, Location
class Weather:

	def __init__(self, user_input: ApiRequest):
		self.user_request = user_input	
		self.response, self.status_code = self.call_api()
		self.error = None
		
		if self.status_code == 401:
			raise InvalidApiKey

		if "error" in self.response:
			self.error = self.response['error']['message']
			return 
		
		self.forecast = Forecast(**self.response["forecast"])
		
		self.data = {
					"city": [],
					"country": [],
					"date": [],
					"min_temp": [],
					"max_temp": [],
					"avg_temp": [],
					"humidity": []
					}
		
		self.parse_defined_forecast()
	
	def call_api(self) -> Union[dict, int]:
		
		api_request = OpenApi(self.user_request)
		return api_request.response, api_request.status_code



	def parse_defined_forecast(self) -> None:
		
			"""
			in daily_parser and location_parser:
			parsing the data into the data dictionary attribute,
			Forecast class has a pydantic to build the data
			for each day based on the json response from the API
			"""
			self.daily_parser()
			self.location_parser()


	def daily_parser(self) -> None:

		"""
		forecast.day is repeatable to retrieve the data, 
		combining it to a static varaiable, 
		the "day" attribute in ForecastDay has the weather data
		from the json response, applied by pydantic library

		"""	
		
		for forecastday in self.forecast.forecastday:
			parse = forecastday.day

			self.data["date"].append(forecastday.date)
			self.data["min_temp"].append(parse.mintemp_c)
			self.data["max_temp"].append(parse.maxtemp_c)
			self.data["avg_temp"].append(parse.avgtemp_c)
			self.data["humidity"].append(parse.avghumidity)


	def location_parser(self) -> None:

		location = Location(**self.response["location"])

		self.data["city"].append(location.name)
		self.data["country"].append(location.country)


