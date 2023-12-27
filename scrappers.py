from experianScrapper import getData as getDataExperian
from dealernetScrapper import getData as getDataDealernet
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Equifax is not working because it requires a captcha
# from equifaxScrapper import getData as getDataEquifax

def run_scrappers(rut):

    # Get current working directory
    current_directory = os.getcwd()
    prefs = {"download.default_directory": current_directory}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('prefs', prefs)

    load_dotenv()

    if os.getenv('DEVELOPMENT') == "True":
        # Chromdriver path in local
        chrome_driver_path=ChromeDriverManager().install()
    else:
        # Chromdriver path in server
        chrome_driver_path='/usr/bin/chromedriver'

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Maximize and zoom out the window
    driver.maximize_window()
    driver.execute_script("document.body.style.zoom='80%'")

    # Get the data for the rut
    rut_socio = getDataExperian(driver, rut)
    getDataDealernet(driver, rut, rut_socio)
    
    # Close the driver
    driver.close()