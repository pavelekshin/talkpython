import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # replaced Firefox by Chrome
driver.get("https://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.CLASS_NAME, "search-field")
elem.clear()
elem.send_keys("pycon")
elem.submit()
assert "No results found." not in driver.page_source
time.sleep(5)  # Let the user actually see something!
driver.close()
