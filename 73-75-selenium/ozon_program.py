import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

# Set Chrome to open in headless mode
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.3987.163 Safari/537.36"
)
options.headless = True
driver = webdriver.Chrome(options=options)  # replaced Firefox by Chrome
driver.get("https://www.ozon.ru")
assert "OZON" in driver.title
elem = driver.find_element(By.NAME, "text")
elem.clear()
elem.send_keys("bjorn dhalie")
elem.submit()
assert "No results found." not in driver.page_source
time.sleep(15)  # Let the user actually see something!
driver.close()
