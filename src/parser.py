from pydantic import BaseModel
from typing import Union, List

class Location(BaseModel):

	name: str
	country: str

class Daily(BaseModel):
	
	maxtemp_c: float
	mintemp_c: float
	avgtemp_c: float
	avghumidity: Union[float, int]

class ForecastDay(BaseModel):
	date: str
	day: Daily

class Forecast(BaseModel):

	forecastday: List[ForecastDay]
