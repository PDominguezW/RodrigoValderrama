from selenium import webdriver
from multiprocessing import Process, Value

from dealernetScrapper import getData as getDataDealernet
from experianScrapper import getData as getDataExperian
from equifaxScrapper import getData as getDataEquifax
import os
from fastapi import FastAPI
import uvicorn

from selenium import webdriver
from dotenv import load_dotenv

from selenium.webdriver.firefox.service import Service

# Create a shared flag to indicate when scraping is ready
scraping_ready = Value('i', 0)

# Create a function to run each scraping task
def run_scraping_task(get_data_function, parameter):

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
    
    get_data_function(driver, parameter)  # Pass the parameter to the scraping function
    driver.quit()

    # Mark the scraping as ready
    with scraping_ready.get_lock():
        scraping_ready.value += 1

def run_scrappers(rut):
    # Create a list of scraping tasks
    # scraping_tasks = [getDataDealernet, getDataExperian, getDataEquifax]
    scraping_tasks = [getDataExperian]

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

app = FastAPI()

@app.get("/{rut}")
async def root(rut: str):
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

    # Create a json with the data of 'dealernet.json', 'experian.json' and 'equifax.json'
    data = {}
    with open('dealernet.json') as json_file:
        data['dealernet'] = json_file.read()
    with open('experian.json') as json_file:
        data['experian'] = json_file.read()
    with open('equifax.json') as json_file:
        data['equifax'] = json_file.read()

    return data
    
if __name__ == "__main__":
    # Run fatstapi
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
