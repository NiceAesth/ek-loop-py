from enum import IntEnum
from enum import unique

from . import build_request

SPEED_OFFSET = 14
RED_OFFSET = 16
GREEN_OFFSET = 17
BLUE_OFFSET = 18


@unique
class SpeedMode(IntEnum):
    SLOWEST = 0x00
    SLOWER = 0x0C
    SLOW = 0x19
    SLOWISH = 0x25
    NORMAL = 0x32
    FASTISH = 0x3E
    FAST = 0x4B
    FASTER = 0x57
    FASTEST = 0x64


@unique
class RGBMode(IntEnum):
    STATIC = 0
    BREATHING = 1
    FADING = 2
    MARQUEE = 3
    COVERING_MARQUEE = 4
    PULSE = 5
    WAVE = 6
    ALTERNATING = 7
    CANDLE = 8


def build_rgb_request(
    color: tuple[int, int, int],
    mode: RGBMode,
    speed: SpeedMode,
) -> bytearray:
    """Builds a request to set the RGB mode and speed.

    Args:
        mode (RGBMode): The mode to set the RGB to.
        speed (SpeedMode): The speed to set the RGB to.
    """
    if mode is RGBMode.STATIC:
        speed = SpeedMode.SLOWEST

    header = bytes(
        [0x10, 0x12, 0x29, 0xAA, 0x01, 0x10, 0xA2, 0x60, 0x00, 0x10, 0x20, 0x01],
    )
    payload = bytearray([mode + 1, 0x00, speed, 0x64])

    request = build_request(header, payload)
    request[RED_OFFSET] = color[0]
    request[GREEN_OFFSET] = color[1]
    request[BLUE_OFFSET] = color[2]
    request[47] = 0xFF
    request[48] = 0x00
    return request
