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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium_recaptcha_solver import RecaptchaSolver

def getData(driver, rut):
    driver.get("https://sec.equifax.cl/clients/")
    time.sleep(10)

    usuario = "PPAUL.FAC"
    password = "Morosa.2024"
    rut="20444718-7"

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
                print(e)
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
    time.sleep(5)

    # Take screen capture
    driver.save_screenshot("equifax.png")
