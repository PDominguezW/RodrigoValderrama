from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import shutil
import glob
import os

def getData(driver, rut):
    driver.get(" https://suite.dealernet.cl")
    time.sleep(5)

    usuario = "LIQUIDEZ.RValderrama"
    password = "benjamin21"
    rut="20444718-7"

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
    time.sleep(15)

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

    # Take screen capture
    driver.save_screenshot("dealernet.png")

    # Search span with title 'Exportar a Pdf'
    element = driver.find_element(By.XPATH, "//div[@class='top-viewer-toolbar']")

    # Get all sub span
    elements = element.find_elements(By.XPATH, ".//span")

    # Click the third span
    elements[2].click()

    # Get the location of the Download folder
    home_directory = os.path.expanduser("~")
    path = os.path.join(home_directory, "Downloads")

    # Get the latest file in the Downloads folder
    latest_file = max(glob.glob(path + "/*.pdf"), key=os.path.getctime)

    # Get the name
    name = os.path.basename(latest_file)
    print(name)

    # Get the path to this project folder
    project_directory = os.path.dirname(os.path.abspath(__file__))

    print(latest_file, project_directory)

    # Move the file to the project folder
    shutil.move(latest_file, project_directory)

    # Changue the name to the file
    os.rename(os.path.join(project_directory, name), os.path.join(project_directory, "dealernet.pdf"))

