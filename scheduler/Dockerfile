FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y cron

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

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R +x ./scripts

ENTRYPOINT ["sh", "./entrypoint.sh"] 
