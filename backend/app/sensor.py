from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from .serializers import SerializedSensorInput
from .orm_models import DbSensorInput


async def backend_write_sensor_input(engine, input: SerializedSensorInput):
    # If there is a LOT of sensor data, this can block the database
    with Session(engine) as session:
        db_input = DbSensorInput(
            machine=input.machine, vibration_speed=input.vibration_speed, timestamp=input.timestamp
        )
        session.add(db_input)
        session.commit()
    return input


async def backend_read_sensor_data(engine, seconds: int) -> List[SerializedSensorInput]:
    now = datetime.now()
    then = datetime.now() - timedelta(seconds=seconds)
    query = select(DbSensorInput).where(DbSensorInput.timestamp.between(then, now))
    result = []
    with Session(engine) as session:
        for sensor_input in session.scalars(query):
            result.append(
                SerializedSensorInput(
                    machine=sensor_input.machine,
                    vibration_speed=sensor_input.vibration_speed,
                    timestamp=sensor_input.timestamp,
                )
            )
    return result
