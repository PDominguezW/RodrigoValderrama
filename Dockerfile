# Get chrome image
FROM selenium/standalone-chrome

COPY dealernetScrapper.py equifaxScrapper.py experianScrapper.py requirements.txt main.py .env ./

USER root
RUN apt-get update && apt-get install python3-distutils -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install -r requirements.txt

# Intall ffmpeg
RUN apt-get install -y ffmpeg

# RUN main.py
CMD ["python3", "main.py"]
