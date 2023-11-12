from selenium import webdriver
from multiprocessing import Process, Value
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, send_file
from selenium.webdriver.common.by import By

from experianScrapper import getData as getDataExperian
from equifaxScrapper import getData as getDataEquifax
from dealernetScrapper import getData as getDataDealernet
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from score_calculator import calculate_score
from utils import fill_and_clean_data, create_data_and_clean, validar_rut

def run_scrappers(rut):

    # Set drivers -------------------------------------------------------

    # Get current working directory
    current_directory = os.getcwd()
    prefs = {"download.default_directory": current_directory}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('prefs', prefs)

    # Search if chrome driver 
    chrome_driver_path='/usr/bin/chromedriver'

    # Create a ChromeDriver service object
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    # --------------------------------------------------------------------

    rut_socio = getDataExperian(driver, rut)

    getDataDealernet(driver, rut, rut_socio)
    
    # Close the driver
    driver.close()

# Create the Flask app
app = Flask(__name__)

@app.route("/", methods=['GET'])
def welcome():
    return "Welcome to the Liquidez API!"

@app.route("/<rut>", methods=['GET'])
def root(rut):

    if rut == "favicon.ico":
        return ""
    
    # Validate the rut
    if not validar_rut(rut):
        return "Rut invalido"

    # Run the main function with the provided parameter and wait until it's over
    run_scrappers(rut)

    # Create a JSON response with the data of 'dealernet.json', 'experian.json', and 'equifax.json'.
    data = create_data_and_clean()

    # Format data
    data = fill_and_clean_data(data)

    # Calculate the score
    file_name = calculate_score(rut, data)

    print("Ejecucion terminada")
    
    return send_file(file_name, as_attachment=True, download_name=file_name)

if __name__ == "__main__":
    # Run Flask app
    from waitress import serve
    serve(app,host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
