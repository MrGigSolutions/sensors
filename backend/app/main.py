from typing import Annotated, List

from fastapi import Depends

from .setup_fastapi import setup_backend
from .setup_alchemy import setup_sql_alchemy

from .login import backend_login, OAuth2PasswordRequestForm
from .sensor import backend_write_sensor_input, backend_read_sensor_data
from .serializers import SerializedSensorInput

app = setup_backend()
engine = setup_sql_alchemy()

@app.post("/auth/token", tags="oauth2")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await backend_login(form_data)

@app.post("/sensor/input/", tags=["sensor","input"])
async def sensor_input(input: SerializedSensorInput) -> SerializedSensorInput:
    return await backend_write_sensor_input(engine, input)

@app.get("/sensor/data", tags=["sensor", "data"])
async def read_sensor_data(seconds: int) -> List[SerializedSensorInput]:
    return await backend_read_sensor_data(engine, seconds)
