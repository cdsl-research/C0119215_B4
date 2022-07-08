FROM locustio/locust@sha256:78148a8b40d012f29d7f274a72e347552e373d740275b7e2f455e70e11c4e9b1
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less psmisc

RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt update
RUN apt install google-chrome-stable -y
RUN apt install openjdk-11-jdk -y

RUN wget https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.0.0-beta-4/selenium-server-4.0.0-beta-4.jar

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install locust-plugins
RUN pip install webdriver-manager
RUN pip install chromedriver-binary-auto
RUN pip install Faker

ENV PATH $PATH:/usr/local/lib/python3.8/site-packages/chromedriver_binary
RUN echo $PATH

#imageで設定されているエントリーポイントをリセット
ENTRYPOINT [""]