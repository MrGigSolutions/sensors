FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /
RUN mkdir /opt/sensor
COPY requirements.txt /opt/sensor/requirements.txt
WORKDIR /opt/sensor
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY source/* .

CMD ["celery", "-A", "tasks", "worker", "--loglevel=INFO"]
