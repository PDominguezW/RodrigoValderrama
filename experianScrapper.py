from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time
from webdriver_manager.chrome import ChromeDriverManager
import json
import traceback
import os
import img2pdf
from parameters import EXPERIAN_USER, EXPERIAN_PASSWORD, EXPERIAN_RESPUESTA_PREGUNTAS

def take_full_screenshot(driver, file_name):
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    images = []

    for i in range(0, total_height, driver.execute_script("return window.innerHeight")):
        # Scroll to next viewport height
        driver.execute_script(f"window.scrollTo(0, {i});")
        # Take screenshot and append to images list
        images.append(driver.get_screenshot_as_png())

    # Scroll back to top of the page
    driver.execute_script("window.scrollTo(0, 0);")

    # Convert the images into a single pdf file, with name file_name
    # and save it in the respaldo folder
    with open(os.path.join("respaldo", file_name), "wb") as f:
        f.write(img2pdf.convert(images))
        
    return 0

def extractDataFromTable(driver, rut, business):

    # Search items in the frame of name 'main'
    time.sleep(5)
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

    if business:
        take_full_screenshot(driver, "experian_business.pdf")
    else:
        take_full_screenshot(driver, "experian_socio.pdf")

    print("Experian: Extracting data")

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
        data['resumen_morosidad']['nro_acreedores'] = 0
        data['resumen_morosidad']['total_doc_impagos'] = 0
        data['resumen_morosidad']['total_pesos'] = 0

    try:
        # Get the text that says 'Bienes Raices'
        element = body.find_element(By.XPATH, "//td[text()='Bienes Raices']")

        # Get the next td element
        element = element.find_element(By.XPATH, "./following-sibling::td")

        # Get the text of the element
        data['resumen_bic']['bienes_raices'] = element.text
    
    except Exception as e:
        data['resumen_bic']['bienes_raices'] = 0

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
        data['resumen_avaluo_bienes_raices']['total_protestos_y_documentos'] = 0
        data['resumen_avaluo_bienes_raices']['total_en_pesos'] = 0

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

    return data

def getData(driver, rut, recursion_depth=0):
    print("Experian: Getting data from experian.cl")
    
    try:

        driver.get("https://transacs.experian.cl/transacs/experian/login.asp")
        time.sleep(5)

        usuario = EXPERIAN_USER
        password = EXPERIAN_PASSWORD
        respuesta = EXPERIAN_RESPUESTA_PREGUNTAS

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

        print("Experian: Logged in")

        data = extractDataFromTable(driver, rut, business=True)

        # Si hay socio
        if data['resumen_socios_sociedades']['rut_socio'] != None and data['resumen_socios_sociedades']['rut_socio'] != "":
            rut_socio = data['resumen_socios_sociedades']['rut_socio']
            
            # Make the driver go back one page
            driver.back()

            # Reload the page, clean the cache
            driver.refresh()

            time.sleep(5)

            data['resumen_socios_sociedades']['data'] = extractDataFromTable(driver, rut_socio, business=False)

        # Write the data in a json file
        with open('experian.json', 'w') as outfile:
            json.dump(data, outfile)

        print("Experian: experian.json created")
        print("Experian: experian.cl finished")

        return data['resumen_socios_sociedades']['rut_socio']
    
    except Exception as e:
        print("Experian: Error in experianScrapper.py")
        # Print traceback
        traceback.print_exc()

        # If recursion depth is 0, try again
        if recursion_depth == 0:
            getData(driver, rut, recursion_depth+1)
        else:
            print("Experian: Error in experianScrapper.py")
            print("Experian: experian.cl finished")
            return None

if __name__ == "__main__":

    # Set drivers -------------------------------------------------------
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")

    # Search if chrome driver 
    chrome_driver_path='/usr/bin/chromedriver'

    # Create a ChromeDriver service object
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    getData(driver, "11.691.672-K")

    driver.quit()