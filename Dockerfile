# Get chrome image
FROM selenium/standalone-chrome

COPY modelo_evaluacion.xlsx Tabla_SII.xlsx score_calculator.py utils.py empty_data.json dealernetScrapper.py equifaxScrapper.py experianScrapper.py requirements.txt main.py ./

USER root
RUN apt-get update

# Install git
RUN apt-get install -y git

# Install pip
RUN apt-get install -y python3-pip
RUN python3 -m pip install -r requirements.txt

# Intall ffmpeg
RUN apt-get install -y ffmpeg

# RUN main.py
CMD ["python3", "main.py"]
