# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver = Chrome(executable_path=r"F:\Downloads\chromedriver.exe")

geolocation = {"latitude": 30.2712, "longitude": 120.1633, "accuracy": 80}
driver.execute_cdp_cmd("Page.setGeolocationOverride", geolocation)
driver.get("https://map.baidu.com")
print()

# geolocation = {"location": {"latitude": 30.2712, "longitude": 120.1633}}
# driver.execute(Command.SET_LOCATION, geolocation)
# driver.get("https://map.baidu.com")
print()

