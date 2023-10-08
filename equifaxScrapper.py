from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import shutil
import glob
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium_recaptcha_solver import RecaptchaSolver
from dotenv import load_dotenv
import json
from webdriver_manager.chrome import ChromeDriverManager
# Import Service from Chrome
from selenium.webdriver.chrome.service import Service
import traceback
import codecs


def getData(driver, rut):
    driver.get("https://sec.equifax.cl/clients/")
    time.sleep(10)

    usuario = "PPAUL.FAC"
    password = "Morosa.2024"

    while True:
        try:
            driver.get("https://sec.equifax.cl/clients/")
            time.sleep(10)
            # Try to close modal
            # Click at 100,100
            ActionChains(driver).move_by_offset(100, 100).click().perform()
            time.sleep(5)

            # Search input with id 'username'
            element = driver.find_element(By.XPATH, "//input[@id='username']")
            element.send_keys(usuario)

            # Search input with id 'password'
            element = driver.find_element(By.XPATH, "//input[@id='password']")
            element.send_keys(password)

            solver = RecaptchaSolver(driver=driver)

            try:
                recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
                solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            except Exception as e:
                time.sleep(5)

            # Find form with name 'loginForm'
            element = driver.find_element(By.XPATH, "//form[@name='loginForm']")

            # Find button inside
            element = element.find_element(By.XPATH, "//button[@type='submit']")
            element.click()
            break
        except Exception as e:
            continue

    # Wait 5 seconds
    time.sleep(10)

    # Get this link: https://sec.equifax.cl/administracionAnfac/anfac
    driver.get("https://sec.equifax.cl/administracionAnfac/anfac")

    # Input with id 'rut'
    element = driver.find_element(By.XPATH, "//input[@id='rut']")
    element.send_keys(rut)

    # Find button with text 'Consultar'
    element = driver.find_element(By.XPATH, "//button[text()='Consultar']")
    element.click()

    # Wait 5 seconds
    time.sleep(10)

    # ------------------------------------------
    # Start data extraction
    # ------------------------------------------

    # Create data dictionary
    data = {}

    # Get 'Detalle Cartera como Cliente'
    try:
        # Find div with id 'ection 1'
        element = driver.find_element(By.XPATH, "//div[@id='ection 1']")

        # Find the table children of element
        table_element = element.find_element(By.XPATH, ".//table")

        # Get the table header (column names)
        header_row = table_element.find_element(By.XPATH, './/thead/tr')
        headers = [header.text for header in header_row.find_elements(By.TAG_NAME, 'th')]

        # Initialize an empty list to store dictionaries
        table_data = {}

        # Iterate through the table rows and create a dictionary for each row
        rows = table_element.find_elements(By.XPATH, './/tbody/tr')

        # If there is only 1 row, then there is no data
        if len(rows) == 1:
            table_data = None
        else:
            for row in rows:
                # Assuming you already have "row" defined as a WebElement
                row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]

                # Create a dictionary for character replacements
                char_replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}

                # Make the character replacements for each cell text within row_data
                row_data[0] = [char_replacements.get(char, char) for char in row_data[0]]
                row_data[0] = ''.join(row_data[0])

                # Assign the first element of row_data as the key for the dictionary
                row_name = row_data[0]
                partial_data = {}
                for i in range(len(headers)):
                    if 'Inst' in headers[i]:
                        headers[i] = 'N.Inst'
                    partial_data[headers[i]] = row_data[i+1]

                table_data[row_name] = partial_data
    
    except Exception as e:
        table_data = None

    data['detalle_cartera_como_cliente'] = table_data

    # Get 'Detalle Cartera como Deudor'
    try:
        # Find div with id 'section 2'
        element = driver.find_element(By.XPATH, "//div[@id='section 2']")

        # Find the table children of element
        table_element = element.find_element(By.XPATH, ".//table")

        # Get the table header (column names)
        header_row = table_element.find_element(By.XPATH, './/thead/tr')
        headers = [header.text for header in header_row.find_elements(By.TAG_NAME, 'th')]

        # Pop first element
        headers.pop(0)

        # Initialize an empty list to store dictionaries
        table_data = {}

        # Iterate through the table rows and create a dictionary for each row
        rows = table_element.find_elements(By.XPATH, './/tbody/tr')

        # If there is only 1 row, then there is no data
        if len(rows) == 1:
            table_data = None
        else:
            for row in rows:
                # Assuming you already have "row" defined as a WebElement
                row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]

                # Create a dictionary for character replacements
                char_replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}

                # Make the character replacements for each cell text within row_data
                row_data[0] = [char_replacements.get(char, char) for char in row_data[0]]
                row_data[0] = ''.join(row_data[0])

                # Assign the first element of row_data as the key for the dictionary
                row_name = row_data[0]
                partial_data = {}
                for i in range(len(headers)):

                    if 'Inst' in headers[i]:
                        headers[i] = 'N.Inst'

                    partial_data[headers[i]] = row_data[i+1]

                table_data[row_name] = partial_data
    
    except Exception as e:
        table_data = None

    data['detalle_cartera_como_deudor'] = table_data

    # Write data in json file
    with open('equifax.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":

    chrome_options = webdriver.ChromeOptions()

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    getData(driver, "96.770.100-9")

    driver.quit()
