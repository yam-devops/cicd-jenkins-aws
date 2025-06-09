from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest

messages = { "should found location": "this should be True, this should be valid location",
			"should not found location": "this should be False, this should be invalid location"
			}

URL = "http://127.0.0.1:5000"


@pytest.fixture(scope="module")
def driver():
	"""Setup WebDriver before tests and close it after tests"""
	options = webdriver.ChromeOptions()
	options.add_argument("--headless=new")
	driver = webdriver.Chrome(options=options)
	yield driver 
	driver.quit()

@pytest.mark.parametrize("location, days, expected_result", [
	("Haifa", 4, True),
	("2eewf", 2, False)
	])

def test_location(driver, location, days, expected_result):
	
	driver.implicitly_wait(2)
	driver.get(URL)

	search_box = driver.find_element(By.NAME, "city")
	search_box.clear()
	search_box.send_keys(location)

	days_box = driver.find_element(By.NAME, "days")
	days_box.send_keys(days)

	submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
	submit_button.click()

	if expected_result:
		try:
			header_text = driver.find_element(By.TAG_NAME, "h1").text
			assert location.title() in header_text, f"Expected location '{location}' in header, but got '{header_text}'"
			assert "weather" in header_text.lower(), f"Expected 'weather' in header, but got '{header_text}'"
		
		except:

			assert False, messages["should found location"]

	else:
		try:
			error_message = driver.find_element(By.XPATH, "//p[@style='color: red;']").text
			assert "no matching location" in error_message.lower(), messages["should not found location"]
		
		except:
			assert False, messages["should not found location"]
		

