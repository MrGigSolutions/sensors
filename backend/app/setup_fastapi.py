from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

TITLE = "Machine vibration simulator"
DESCRIPTION = """# Machine Vibration Simulator
This backend simulates how inputs may be used to generate reports on a
frontend, by using the following technology stacks:
Python, SQLAlchemy, FastAPI, Celery, PostgreSQL, Pydantic, JavaScript, React, RabbitMQ, Docker

## Sensor Data

You can **read machine data for a provided number of seconds**.
You can **add sensor readings for provided machine**
"""
SUMMARY = "This backend simulates the reporting of sensor data."
ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]
TAGS_METADATA = [
    {
        "name": "sensor",
        "description": "Operations with sensor data.",
    },
    {
        "name": "oauth",
        "description": "Perform a login using an OAuth2 standard.",
    },
]


def setup_backend():
    app = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        summary=SUMMARY,
        openapi_tags=TAGS_METADATA,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
