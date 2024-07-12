from typing import Annotated, List

from fastapi import Depends

from .login import OAuth2PasswordRequestForm, backend_login
from .sensor import backend_read_sensor_data, backend_write_sensor_input
from .serializers import SerializedSensorInput
from .setup_alchemy import setup_sql_alchemy
from .setup_fastapi import setup_backend

app = setup_backend()
engine = setup_sql_alchemy()


@app.post("/auth/token", tags=["oauth"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await backend_login(form_data)


@app.post("/sensor/input/", tags=["sensor"], description="Post sensor data")
async def sensor_input(input: SerializedSensorInput) -> SerializedSensorInput:
    return await backend_write_sensor_input(engine, input)


@app.get("/sensor/data", tags=["sensor"], description="Retrieve sensor data")
async def read_sensor_data(seconds: int) -> List[SerializedSensorInput]:
    return await backend_read_sensor_data(engine, seconds)
