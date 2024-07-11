FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# --- Install Postgres client ---
RUN apk add postgresql

WORKDIR /
RUN mkdir /opt/backend
COPY requirements.txt /opt/backend/requirements.txt
WORKDIR /opt/backend
RUN pip3 install -r requirements.txt

COPY app/* ./app/
COPY run.sh ./
RUN chmod +x ./run.sh

CMD ["/opt/backend/run.sh"]
