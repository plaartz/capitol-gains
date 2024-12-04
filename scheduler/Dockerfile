FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade && apt-get install -y cron && apt-get install -y wget

RUN echo "America/Central" > /etc/timezone
RUN DEBIAN_FRONTEND=noninteractive TZ=America/New_York apt-get -y install tzdata
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN dpkg-reconfigure -fnoninteractive tzdata

COPY cron-job /etc/cron.d/cron-job
RUN chmod 0644 /etc/cron.d/cron-job

RUN crontab /etc/cron.d/cron-job

RUN touch /var/log/cron.log

WORKDIR /scheduler
RUN touch logfile.log
RUN mkdir backup

# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
# Detect architecture and install Chrome/Chromium accordingly
RUN dpkgArch="$(dpkg --print-architecture)" && \
    if [ "$dpkgArch" = "amd64" ]; then \
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
        apt-get install -y ./google-chrome-stable_current_amd64.deb; \
    elif [ "$dpkgArch" = "arm64" ]; then \
        apt-get install chromium -y; \
    else \
        echo "Unsupported architecture: $dpkgArch" && exit 1; \
    fi

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R +x ./script

ENTRYPOINT ["sh", "./entrypoint.sh"] 
