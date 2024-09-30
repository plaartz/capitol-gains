FROM python:3.10
ENV PYTHONUNBUFFERED 1

ARG BASE_DIR

EXPOSE 8000

WORKDIR /api

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "./entrypoint.sh"]
