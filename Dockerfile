# Get chrome image
FROM selenium/standalone-chrome:119.0

# Set environment variables
ENV DEVELOPMENT=False
ENV MONGODB_URL=mongodb+srv://telefactor2:telefactor2@telefactor.cdmw70f.mongodb.net/

COPY modelo_evaluacion.xlsx Tabla_SII.xlsx score_calculator.py utils.py empty_data.json dealernetScrapper.py experianScrapper.py requirements.txt main.py scrappers.py parameters.py ./

# Give root permissions
USER root

# Create folder respaldo
RUN mkdir respaldo

RUN apt-get update

# Install git 2.25.1
RUN apt-get install -y --no-install-recommends git

# Install pip
RUN apt-get install -y --no-install-recommends python3-pip

RUN python3 -m pip install -r requirements.txt

# RUN main.py
CMD ["python3", "main.py"]