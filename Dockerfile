FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN mkdir -p /usr/src/
ADD . /usr/src/
WORKDIR /usr/src/
#RUN pip install -r requirements.txt
RUN chmod +x /usr/src/chromedriver
#RUN apt-get -y install chromium-browser
RUN apt-get -y install wget
RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update
RUN apt-get -y install google-chrome-stable
RUN apt-get -y install xvfb
RUN export LC_ALL=C
#RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
#RUN tar -zxvf geckodriver-v0.11.1-linux64.tar.gz
#RUN mv geckodriver /usr/bin/
#RUN export PAHT=$PATH:/usr/bin/

RUN pip install selenium
RUN pip install requests
RUN pip install 'setuptools<20.2'
RUN pip install pyvirtualdisplay

RUN apt-get -y install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
RUN apt-get -y install nano
#RUN cd chilkat
RUN python /usr/src/chilkat/installChilkat.py
