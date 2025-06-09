
# Weather Web App Project

 A weather forecast app based on python, that recieves from a user a city or country and chooses the amount of days to present the forecast up to 10 days.

# Features

Using external API:
- Shows real time weather data for the user-specifed location
- Fetch data for the requested amount of days including:
	- Humidity level
	- Day and night temperature for each day
- Handle errors with custom pages and status codes:
	- Location not found
	- Invalid API key

# Technologies
- Python
- Flask for python http web application and easy page routing and render templates
- Weather API (real time weather web API)
- Logging library for logging requests for and from users & external API, useful for debugging
- Pydantic - used to build the parsing objects and handle errors automatically, very compact and maintainable code
- Unittest and Pytest- mock objects for mocking valid and invalid responses from API for testing
- HTML for custom pages

# Installation & Requirements

- flask
- requests
- pydantic
- Jinja2

To install:
recommended in a virtual environment to ensure package isolation for dependencies  
```
python3 -m venv .venv  
activate - source .venv/bin/activate  
pip install -r requirments.txt
```

# Run Application
The API key file needs to be as environement variable.
Running the server does not rely on the API key, but without it requests will receive `InvalidApiKey` error
```
python3 server.py
```
app runs automtically on web in the url http://127.0.0.1:5000

# Usage
1. Enter the web at browser [http://127.0.0.1:5000 ]
2. Enter a city name and chosse between 1 - 10 forecast days (this is a must to send a POST request) and press submit
3. The backend sends the REST API a request based on the user parameters and parse the json response
4. The frontend then displays the response in a table in HTML in the page /yourforecast with daily dates, temperature and humidity

# Errors

- Invalid Location Error, user recieves a custom page of an invalid location and a button to go back to main menu
- Invalid API key error is checked and user recieves a server error HTML
- 404 not found: a 404 error page HTML when a user enters a page that does not exist with a button to return to main page

