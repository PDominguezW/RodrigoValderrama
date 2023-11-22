# Get chrome image
FROM selenium/standalone-chrome:119.0

COPY modelo_evaluacion.xlsx Tabla_SII.xlsx score_calculator.py utils.py empty_data.json dealernetScrapper.py equifaxScrapper.py experianScrapper.py requirements.txt main.py .env ./

# Give root permissions
USER root

RUN apt-get update

# Install git 2.25.1
RUN apt-get install -y --no-install-recommends git=1:2.25.1-1ubuntu3.1

# Install pip
RUN apt-get install -y --no-install-recommends python3-pip=23.3.1

RUN python3 -m pip install -r requirements.txt

# RUN main.py
CMD ["python3", "main.py"]

# Remove root permissions
USER seluser
