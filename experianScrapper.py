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
from dotenv import load_dotenv
import os
import json

def extractDataFromTable(driver, rut):

    # Search items in the frame of name 'main'
    driver.switch_to.frame("main")

    # Search form with name trans1
    element = driver.find_element(By.XPATH, "//form[@name='trans1']")

    # Input name c_rut_busca_display
    preRut = element.find_element(By.XPATH, "//input[@name='c_rut_busca_display']")
    print(rut)
    print(rut.split("-"))
    preRut.send_keys(rut.split("-")[0])

    # Input name c_dig_busca_display
    postRun = element.find_element(By.XPATH, "//input[@name='c_dig_busca_display']")
    postRun.send_keys(rut.split("-")[1])

    # Input name c_incl_res063
    element = driver.find_element(By.XPATH, "//input[@name='c_atco_99063']")
    element.click()

    # Input name c_incl_res007
    element = driver.find_element(By.XPATH, "//input[@name='c_atco_99007']")
    element.click()

    # Input name c_atco_99243
    element = driver.find_element(By.XPATH, "//input[@name='c_atco_99243']")
    element.click()

    # Input name c_incl_res095
    element = driver.find_element(By.XPATH, "//input[@name='c_atco_99095']")
    element.click()

    # Button name 'corre'
    element = driver.find_element(By.XPATH, "//button[@name='corre']")
    driver.execute_script("arguments[0].click();", element)

    # Sleep 5 seconds
    time.sleep(5)

    # -----------------------------------------------
    # Here we start collecting the data
    # -----------------------------------------------

    data = {
        'resumen_morosidad': {},
        'resumen_bic': {},
        'resumen_avaluo_bienes_raices': {},
        'resumen_socios_sociedades': {}
    }

    # Get the html element inside frame
    body = driver.find_element(By.XPATH, "//html").find_element(By.XPATH, "//body")

    try:
        # Get the td 'Nro de Acreedores'
        element = body.find_element(By.XPATH, "//p[text()='Servicio: Resumen Consolidado de Morosidad']")

        # Get the next table element
        element = element.find_element(By.XPATH, "./following-sibling::table")

        # Get the all the td inside the table
        elements = element.find_elements(By.XPATH, "./tbody/tr/td")

        # Get the text
        data['resumen_morosidad']['nro_acreedores'] = elements[3].text
        data['resumen_morosidad']['total_doc_impagos'] = elements[4].text
        data['resumen_morosidad']['total_pesos'] = elements[5].text

    except Exception as e:
        data['resumen_morosidad']['nro_acreedores'] = None
        data['resumen_morosidad']['total_doc_impagos'] = None
        data['resumen_morosidad']['total_pesos'] = None

    try:

        # Get the text that says 'Bienes Raices'
        element = body.find_element(By.XPATH, "//td[text()='Bienes Raices']")

        # Get the next td element
        element = element.find_element(By.XPATH, "./following-sibling::td")

        # Get the text of the element
        data['resumen_bic']['bienes_raices'] = element.text
    
    except Exception as e:
        data['resumen_bic']['bienes_raices'] = None

    try:
        # Get the p 'Servicio: Resumen BIC - Protestos y Documentos Vigentes'
        element = body.find_element(By.XPATH, "//p[text()='Servicio: Resumen BIC - Protestos y Documentos Vigentes']")

        # Get the next table element
        element = element.find_element(By.XPATH, "./following-sibling::table")

        # Find the last tr inside the table
        element = element.find_element(By.XPATH, "./tbody/tr[last()]")

        # Find the td inside the tr
        elements = element.find_elements(By.XPATH, "./td")

        # Get data
        data['resumen_avaluo_bienes_raices']['total_protestos_y_documentos'] = elements[1].text
        data['resumen_avaluo_bienes_raices']['total_en_pesos'] = elements[2].text

    except Exception as e:
        data['resumen_avaluo_bienes_raices']['total_protestos_y_documentos'] = None
        data['resumen_avaluo_bienes_raices']['total_en_pesos'] = None

    try:
        # Get the p with text 'Servicio: Detalle de Socios'
        element = body.find_element(By.XPATH, "//p[text()='Servicio: Detalle de Socios']")

        # Get the next table element
        element = element.find_element(By.XPATH, "./following-sibling::table")

        # Get the first button on the table
        element = element.find_element(By.XPATH, "./tbody/tr/td/button")
        element.click()

        # Find the td element inside the table, that contains 'Rut Socio'
        element = element.find_element(By.XPATH, "//td[contains(text(),'Rut Socio')]")

        # Get the parent element of element
        element = element.find_element(By.XPATH, "..")

        # Get the next element
        element = element.find_element(By.XPATH, "./following-sibling::tr")

        # Get the text of the first element
        element = element.find_element(By.XPATH, "./td[1]")

        # Get the text
        data['resumen_socios_sociedades']['rut_socio'] = element.text

    except Exception as e:
        data['resumen_socios_sociedades']['rut_socio'] = None

    print(data)

    return data

def getData(driver, rut):
    print("aaaaaaa" + rut)
    driver.get("https://transacs.experian.cl/transacs/experian/login.asp")
    time.sleep(5)

    usuario="dbello"
    password="$iNaCoF1"
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

    data = extractDataFromTable(driver, rut)

    # Si hay socio
    if data['resumen_socios_sociedades']['rut_socio'] != None:
        rut_socio = data['resumen_socios_sociedades']['rut_socio']
        
        # Make the driver go back one page
        driver.back()

        # Reload the page, clean the cache
        driver.refresh()

        time.sleep(5)

        data['resumen_socios_sociedades']['data'] = extractDataFromTable(driver, rut_socio)

    # Write the data in a json file
    with open('experian.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":

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

    getData(driver, "11.691.672-K")

    driver.quit()