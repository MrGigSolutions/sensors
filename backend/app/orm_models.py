from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DbSensorInput(Base):
    __tablename__ = "sensorinput"

    id: Mapped[int] = mapped_column(primary_key=True)
    machine: Mapped[str] = mapped_column(String(30))
    vibration_speed: Mapped[int]
    timestamp: Mapped[datetime]

    def __repr__(self) -> str:
        return (
            f"SensorInput("
            f"id={self.id!r}, "
            f"name={self.machine!r}, "
            f"vibration_speed={self.vibration_speed!r}, "
            f"timestamp={self.timestamp.isoformat()!r} "
            f")"
        )
