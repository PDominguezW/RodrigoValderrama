from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

def getData(driver, rut):
    driver.get("https://transacs.experian.cl/transacs/experian/login.asp")
    time.sleep(5)

    usuario="dbello"
    password="$iNaCoF1"
    rut="20444718-7"
    respuesta="kira"

    # Input id user
    element = driver.find_element(By.XPATH, "//input[@id='user']")
    element.send_keys(usuario)

    # Input id pass
    element = driver.find_element(By.XPATH, "//input[@id='pass']")
    element.send_keys(password)

    # Input id but_user
    element = driver.find_element(By.XPATH, "//input[@id='but_user']")
    element.click()

    # Sleep 5 seconds
    time.sleep(5)

    try:
        # Input id tipo2
        element = driver.find_element(By.XPATH, "//input[@id='tipo2']")
        element.send_keys(respuesta)

        # Input id tipo3
        element = driver.find_element(By.XPATH, "//input[@id='tipo3']")
        element.send_keys(respuesta)

        # Button name Boton
        element = driver.find_element(By.XPATH, "//button[@name='Boton']")
        element.click()

        # Sleep 5 seconds
        time.sleep(5)
    except:
        pass

    # Search items in the frame of name 'main'
    driver.switch_to.frame("main")

    # Search form with name trans1
    element = driver.find_element(By.XPATH, "//form[@name='trans1']")

    # Input name c_rut_busca_display
    preRut = element.find_element(By.XPATH, "//input[@name='c_rut_busca_display']")
    preRut.send_keys(rut.split("-")[0])

    # Input name c_dig_busca_display
    postRun = element.find_element(By.XPATH, "//input[@name='c_dig_busca_display']")
    postRun.send_keys(rut.split("-")[1])

    # Input name c_incl_res063
    element = driver.find_element(By.XPATH, "//input[@name='c_incl_res063']")
    element.click()

    # Input name c_incl_res007
    element = driver.find_element(By.XPATH, "//input[@name='c_incl_res007']")
    element.click()

    # Input name c_atco_99243
    element = driver.find_element(By.XPATH, "//input[@name='c_atco_99243']")
    element.click()

    # Input name c_incl_res095
    element = driver.find_element(By.XPATH, "//input[@name='c_incl_res095']")
    element.click()

    # Button name 'corre'
    element = driver.find_element(By.XPATH, "//button[@name='corre']")
    element.click()

    # Sleep 5 seconds
    time.sleep(5)

    # Take a screen capture
    driver.save_screenshot('experian.png')