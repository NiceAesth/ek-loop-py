from __future__ import annotations

from pydantic import BaseModel

from . import build_request

FAN_COUNT = 6
FAN_CHANNELS = [
    bytearray([0xA0, 0xA0]),
    bytearray([0xA0, 0xC0]),
    bytearray([0xA0, 0xE0]),
    bytearray([0xA1, 0x00]),
    bytearray([0xA1, 0x20]),
    bytearray([0xA1, 0xE0]),
]

FAN_READ_RPM_OFFSET = 12
FAN_READ_PWM_OFFSET = 21


def rpm_to_bytes(rpm: int) -> bytearray:
    """Converts an RPM value to a 2 byte representation.

    Args:
        rpm (int): The RPM value to convert.

    Returns:
        bytearray: The 2 byte representation of the RPM value.
    """
    return bytearray([(rpm >> 8) & 0xFF, rpm & 0xFF])


def bytes_to_rpm(buffer: bytearray) -> int:
    """Converts a 2 byte representation of an RPM value to an integer.

    Args:
        buffer (bytearray): The 2 byte representation of the RPM value.

    Returns:
        int: The integer representation of the RPM value.
    """
    return (buffer[0] << 8) + buffer[1]


def build_speed_read_request(channel: int) -> bytearray:
    """Builds a request to read the fan speed.

    Args:
        channel (int): The channel to read the speed from. (0-5)
    """
    header = bytes([0x10, 0x12, 0x08, 0xAA, 0x01, 0x03])
    payload = FAN_CHANNELS[channel] + bytearray([0x00, 0x20, 0x66, 0xFF, 0xFF, 0xED])
    return build_request(header, payload)


def build_speed_write_request(channel: int, pwm: int, rpm: int = 0) -> bytearray:
    """Builds a request to set the fan speed.

    Args:
        channel (int): The channel to set the speed for. (0-5)
        pwm (int): The PWM value to set the fan to. (0-100%)
        rpm (int, optional): The RPM value to set the fan to. Defaults to 0.
    """
    header = bytes([0x10, 0x12, 0x29, 0xAA, 0x01, 0x10])
    payload = FAN_CHANNELS[channel] + bytearray(
        [0x00, 0x10, 0x20, 0x00, 0x00, 0x00, 0x00],
    )

    rpm_bytes = rpm_to_bytes(rpm) + bytearray([0] * 7)
    pwm_bytes = bytearray([pwm, 0xFF] + [0] * 19)
    checksum_bytes = bytearray([0xFF, 0xED])

    payload.extend(rpm_bytes + pwm_bytes + checksum_bytes)
    return build_request(header, payload)


class SpeedReadResponse(BaseModel):
    channel: int
    pwm: int
    rpm: int

    @classmethod
    def from_buffer(cls, channel: int, buffer: bytearray) -> SpeedReadResponse:
        pwm = buffer[FAN_READ_PWM_OFFSET]
        rpm = bytes_to_rpm(buffer[FAN_READ_RPM_OFFSET : FAN_READ_RPM_OFFSET + 2])
        return cls(channel=channel, pwm=pwm, rpm=rpm)
