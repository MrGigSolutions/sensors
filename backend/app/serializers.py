from datetime import datetime

from pydantic import BaseModel


class SerializedSensorInput(BaseModel):
    # TODO: Limit to 30 char length
    machine: str
    # TODO: Limit between 1 and 5
    vibration_speed: int
    timestamp: datetime

class SerializedDateRange(BaseModel):
    # TODO: Limit this further to prevent massive queries, or
    #       negative ranges
    seconds: int

class SerializedLoggedIn(BaseModel):
    logged_in: bool

class SerializedUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class SerializedUserWithPasswordHash(SerializedUser):
    hashed_password: str