from experianScrapper import getData as getDataExperian
from dealernetScrapper import getData as getDataDealernet
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager

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

    # Chromdriver path in server
    chrome_driver_path='/usr/bin/chromedriver'

    # Create a ChromeDriver service object
    # To run on server:
    service = Service(chrome_driver_path)

    # To run locally:
    # service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Get the data for the rut
    rut_socio = getDataExperian(driver, rut)
    getDataDealernet(driver, rut, rut_socio)
    
    # Close the driver
    driver.close()