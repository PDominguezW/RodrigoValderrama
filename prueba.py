from selenium import webdriver
from multiprocessing import Process, Value
from selenium.webdriver.firefox.service import Service
from dotenv import load_dotenv
import os
from flask import Flask, jsonify

from experianScrapper import getData as getDataExperian
from equifaxScrapper import getData as getDataEquifax
from dealernetScrapper import getData as getDataDealernet
import json
import time


# Create the Flask app
app = Flask(__name__)

@app.route("/<rut>")
def root(rut):

    # Load the .env file
    load_dotenv()

    # If we are in development mode
    if os.getenv('DEVELOPMENT') == 'True':
        executable_path = os.getenv('GECKODRIVER_PATH_DEV')
    else:
        executable_path = os.getenv('GECKODRIVER_PATH_PROD')

    # Create service
    service = Service(executable_path=executable_path)

    # Create driver
    driver = webdriver.Firefox(service=service)

    driver.get("https://www.experian.cl/")
    time.sleep(40)

    return "adios"


if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
