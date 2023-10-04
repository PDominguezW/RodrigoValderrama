FROM ubuntu:22.04

WORKDIR /app

COPY dealernetScrapper.py equifaxScrapper.py experianScrapper.py requirements.txt main.py ./

RUN apt-get update && \
    apt-get install -y wget

# Install firefox -----------
RUN apt-get update && \
    apt-get install -y wget

# Install bzip
RUN apt-get install -y bzip2 && \
    apt-get install -y xvfb && \
    apt-get install -y libpci-dev && \
    apt-get install -y vim

# Install Firefox
ENV FF_VER 105.0
ENV FF_DIR /dist
RUN apt update -y && apt upgrade -y && apt install -y libgtk-3-common libasound2 libdbus-glib-1-2
RUN mkdir -p $FF_DIR && cd $FF_DIR && wget -O - https://ftp.mozilla.org/pub/firefox/releases/$FF_VER/linux-x86_64/en-US/firefox-$FF_VER.tar.bz2 | tar -xjf -
ENV PATH $FF_DIR/firefox:$PATH

# Install pip-----------------
RUN apt-get install -y python3-pip
# ----------------------------

# Install Geckodriver---------
RUN apt-get install -y wget && \
    wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    tar -xzf geckodriver.tar.gz && \
    mv geckodriver /usr/local/bin && \
    rm geckodriver.tar.gz && \
    apt-get remove -y wget && \
    apt-get autoremove -y
# ----------------------------

# Intall ffmpeg
# RUN apt-get install -y ffmpeg

# Install python dependencies
RUN pip3 install -r requirements.txt

# Run
ENV DISPLAY :99
ENV PORT 8080

ADD run.sh /run.sh
RUN chmod a+x /run.sh

CMD /run.sh
