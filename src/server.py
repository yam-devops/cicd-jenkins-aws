import requests
from flask import Flask, render_template, request, Response
import web_logger
from forecast_builder import Weather
from open_api import ApiRequest
from prometheus_client import generate_latest, Counter, Gauge, Histogram

app = Flask(__name__)

REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")
city_requests_counter = Counter(
    "city_requests_total", "Total number of requests for a city", ["city"]
)

@app.get('/')
def main_menu():


	REQUEST_COUNT.inc()
	return render_template("index.html")

	

@app.route('/yourforecast', methods=['POST'])
def dispaly_forecast():

	city = request.form['city']
	days = int(request.form['days'])

	user_request = ApiRequest(city=city, days=days) 
	forecast = Weather(user_request)

	if forecast.error != None:
		
		return render_template("error.html", error = forecast.error), forecast.status_code	

	city_requests_counter.labels(city=city).inc()

	return render_template("forecast.html", data=forecast.data, DAYS=days)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")



@app.errorhandler(404)
def not_found_error(error):
	
	return render_template("404.html", error=error), 404


@app.errorhandler(500)
def server_error(error):
	
	return render_template("server_error.html", error=error), 500


if __name__ == '__main__':

	app.run(host="0.0.0.0",debug=False)
