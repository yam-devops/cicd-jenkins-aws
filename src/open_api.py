import os
import requests
from dataclasses import dataclass

API_KEY = os.getenv("WEATHER_API_KEY")


@dataclass
class ApiRequest():
	
	city: str
	days: int


class OpenApi():

	def __init__(self, Api_request: ApiRequest):
		
		self.Api_request = Api_request
		self.response, self.status_code = self.open_url()
		

	def open_url(self) -> tuple:

		url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={self.Api_request.city}&days={self.Api_request.days}&aqi=no&alerts=no"
		response = requests.get(url)

		return response.json(), response.status_code


class InvalidApiKey(Exception):
	def __str__(self):
		
		return f"invalid API key, {API_KEY}"

