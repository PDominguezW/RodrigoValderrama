from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import shutil
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import pdfplumber
import json
import glob
import traceback

def getData(driver, rut):
    try:
        driver.get(" https://suite.dealernet.cl")
        time.sleep(5)

        usuario = "LIQUIDEZ.RValderrama"
        password = "benjamin21"

        # Search input with id='uname'
        element = driver.find_element(By.XPATH, "//input[@name='uname']")
        element.send_keys(usuario)

        # Search input with id='psw'
        element = driver.find_element(By.XPATH, "//input[@name='psw']")
        element.send_keys(password)

        # Search button with class='login-button'
        element = driver.find_element(By.XPATH, "//button[@class='login-button']")
        element.click()

        # Wait 5 seconds
        time.sleep(10)

        # Reload page
        driver.refresh()

        # Wait 5 seconds
        time.sleep(10)

        # Search span with text 'Central de Informacion'
        element = driver.find_element(By.XPATH, "//span[text()='Central de Informacion']")
        element.click()

        # Wait 5 seconds
        time.sleep(5)

        # Input with id='rut'
        element = driver.find_element(By.XPATH, "//input[@id='rut']")
        element.send_keys(rut)

        # Search label with text 'Comportamiento Vigente'
        element = driver.find_element(By.XPATH, "//label[text()='Comportamiento Vigente']")
        element.click()

        # Search div that text contains text 'Realizar consulta'
        element = driver.find_element(By.XPATH, "//div[contains(text(),'Realizar consulta')]")
        element.click()

        # Wait 5 seconds
        time.sleep(5)

        # Search span with text 'Ver'
        element = driver.find_element(By.XPATH, "//span[text()='Ver']")
        element.click()

        # Wait 5 seconds
        time.sleep(10)

        # Changue to the new tab
        driver.switch_to.window(driver.window_handles[1])

        # Search span with title 'Exportar a Pdf'
        element = driver.find_element(By.XPATH, "//div[@class='top-viewer-toolbar']")

        # Get all sub span
        elements = element.find_elements(By.XPATH, ".//span")

        # Click the third span
        elements[2].click()

        time.sleep(5)

        # Find all the files in this folder
        current_directory = os.getcwd()
        pdf_file = glob.glob(current_directory + "/*.pdf")[0]

        # Changue the name of the pdf to 'dealernet.pdf'
        os.rename(pdf_file, current_directory + "/dealernet.pdf")

        # Extract table info from pages 0 and 1, using pdfplumber
        with pdfplumber.open("dealernet.pdf") as pdf:
            page = pdf.pages[0]
            table = page.extract_table()

            page = pdf.pages[1]
            table2 = page.extract_table()

            # Add info from page 1 to page 0
            table.extend(table2)
            
        # Define the character replacements dictionary for uppercase characters
        char_replacements = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'N'}

        # Initialize the resulting dictionary
        result_dict = {}

        # Get the headers and remove the first column ('VARIABLES/PERIODOS')
        headers = table[0][1:]

        # Loop through the table rows and create the nested dictionary
        for row in table[1:]:
            variable_name = row[0].replace('\n', ' ')  # Replace '\n' with space and handle uppercase characters
            for uppercase_char, replacement in char_replacements.items():
                variable_name = variable_name.replace(uppercase_char, replacement)
            variable_data = {header: value for header, value in zip(headers, row[1:])}
            result_dict[variable_name] = variable_data


        # Write the result to a json file
        with open('dealernet.json', 'w') as outfile:
            json.dump(result_dict, outfile)

        print("dealernet.json created")
    except Exception as e:
        print("Error in dealernetScrapper.py")
        traceback.print_exc()

if __name__ == "__main__":

    chrome_options = webdriver.ChromeOptions()

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    getData(driver, "96.770.100-9")