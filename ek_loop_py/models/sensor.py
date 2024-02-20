from __future__ import annotations

from enum import IntEnum
from enum import unique

from pydantic import BaseModel

from . import build_request

TEMP_SENSOR_COUNT = 3
L_H_MULTIPLIER = 0.8


@unique
class LevelWarnings(IntEnum):
    WARNING = 0
    OPTIMAL = 1 << 6


def build_sensor_read_request() -> bytearray:
    """Builds a request to read the fan speed.

    Args:
        channel (int): The channel to read the speed from. (0-5)
    """
    header = bytes([0x10, 0x12, 0x08, 0xAA, 0x01, 0x03])
    payload = bytearray([0xA2, 0x20, 0x00, 0x20, 0x66, 0xFF, 0xFF, 0xED])
    return build_request(header, payload)


class SensorReadResponse(BaseModel):
    t1_temp: int
    """The temperature of the first sensor. (°C)"""
    t2_temp: int
    """The temperature of the second sensor. (°C)"""
    t3_temp: int
    """The temperature of the third sensor. (°C)"""
    flow: float
    """The flow rate in liters per hour."""
    coolant_status: LevelWarnings
    """The status of the coolant level."""

    @classmethod
    def from_buffer(cls, buffer: bytearray) -> SensorReadResponse:
        t1_temp = buffer[11]
        t2_temp = buffer[15]
        t3_temp = buffer[19]

        flow = float((buffer[22] << 16) + (buffer[23] << 8) + buffer[24])
        flow *= L_H_MULTIPLIER

        coolant_status = LevelWarnings(buffer[27])

        return cls(
            t1_temp=t1_temp,
            t2_temp=t2_temp,
            t3_temp=t3_temp,
            flow=flow,
            coolant_status=coolant_status,
        )
