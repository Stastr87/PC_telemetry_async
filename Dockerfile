FROM python:3.12.4-slim

COPY . /var/lib/pc_telemetry

WORKDIR /var/lib/pc_telemetry

RUN apt-get -y update && apt-get -y install nano && apt-get install -y tzdata

RUN apt update && apt install -y --no-install-recommends make git

RUN pip3 install --upgrade pip \
    && pip3 install 'pipenv==2024.0.1' \
    && pipenv install --system \
    && pipenv install --dev --system

ENV PYTHONPATH="/var/lib/pc_telemetry"