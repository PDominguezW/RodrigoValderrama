from selenium import webdriver
from multiprocessing import Process, Value
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from selenium.webdriver.common.by import By

from experianScrapper import getData as getDataExperian
from equifaxScrapper import getData as getDataEquifax
from dealernetScrapper import getData as getDataDealernet
import json
import time
from webdriver_manager.chrome import ChromeDriverManager

# Create a shared flag to indicate when scraping is ready
scraping_ready = Value('i', 0)

# Create a function to run each scraping task
def run_scraping_task(get_data_function, parameter):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    get_data_function(driver, parameter)  # Pass the parameter to the scraping function
    driver.quit()

    # Mark the scraping as ready
    with scraping_ready.get_lock():
        scraping_ready.value += 1

def run_scrappers(rut):
    # Create a list of scraping tasks
    # scraping_tasks = [getDataDealernet, getDataExperian, getDataEquifax]
    scraping_tasks = [getDataExperian, getDataEquifax]

    # Create a process for each scraping task
    processes = []

    for task in scraping_tasks:
        process = Process(target=run_scraping_task, args=(task, rut))
        processes.append(process)

    # Start all the processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

# Create the Flask app
app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to the API!"

@app.route("/<rut>")
def root(rut):

    # Reset the scraping ready flag
    global scraping_ready
    scraping_ready = Value('i', 0)

    # Run the main function with the provided parameter and wait until it's over
    run_scrappers(rut)

    # Wait for all scraping processes to finish
    while True:
        with scraping_ready.get_lock():
            if scraping_ready.value == 1:
                break

    # Create a JSON response with the data of 'dealernet.json', 'experian.json', and 'equifax.json'.
    data = {}

    if os.path.isfile('dealernet.json'):
        with open('dealernet.json') as json_file:
            data['dealernet'] = json.load(json_file)
    else:
        data['dealernet'] = None

    if os.path.isfile('experian.json'):
        with open('experian.json') as json_file:
            data['experian'] = json.load(json_file)
    else:
        data['experian'] = None

    if os.path.isfile('equifax.json'):
        with open('equifax.json') as json_file:
            data['equifax'] = json.load(json_file)
    else:
        data['equifax'] = None

    return jsonify(data)

if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
