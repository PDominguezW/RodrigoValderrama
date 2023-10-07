from selenium import webdriver
from multiprocessing import Process, Value
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from selenium.webdriver.common.by import By

import json
import time
from webdriver_manager.chrome import ChromeDriverManager

# Create the Flask app
app = Flask(__name__)

@app.route("/")
def root():
    print("Starting scraping")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get("https://www.experian.cl/")

    # Get all the text on body
    text = driver.find_element(By.XPATH, "//body").text

    return text

if __name__ == "__main__":
    print("Starting Flask app aaaaaaaaaaaa")
    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
