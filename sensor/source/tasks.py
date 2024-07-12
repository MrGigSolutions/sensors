import datetime
import random
import json
from typing import Dict, Any

from celery import Celery
import httpx

app = Celery()
app.config_from_object("sensorconfig")


@app.task(name="tasks.generate_vibration")
def generate_vibration():
    sensor_readings = []
    for machine in load_machines():
        sensor_reading = _get_fake_sensor_reading(machine)
        json_result = json.dumps(sensor_reading)
        # TODO: Make this properly async
        response = httpx.post("http://backend:80/sensor/input/", json=sensor_reading)
        if response.status_code != 200:
            raise RuntimeError(f"Response code {response.status_code} on data '{json_result}'.")
        sensor_readings.append(sensor_reading)
    return sensor_readings


def _get_fake_sensor_reading(machine: str) -> Dict[str, Any]:
    return {
        "machine": machine,
        "vibration_speed": random.randint(1, 5),
        "timestamp": datetime.datetime.now().isoformat(),
    }


def load_machines():
    machine_file = open("/opt/sensor/machines", "r")
    result = []
    try:
        count = 0

        while True:
            count += 1

            # Get next line from file
            line = machine_file.readline()

            # if line is empty
            # end of file is reached
            if not line:
                break
            result.append(line.strip())
    finally:
        machine_file.close()
    return result
