from warnings import warn

from device.ek import EKDevice
from models.rgb import RGBMode
from models.rgb import SpeedMode
from models.rgb import build_rgb_request


class RGBService:

    def __init__(self, ek_dev: EKDevice) -> None:
        self.ek_dev = ek_dev
        self.current_color = (255, 255, 255)
        self.current_mode = RGBMode.STATIC
        self.current_speed = SpeedMode.SLOWEST

    def set_rgb(
        self,
        color: tuple[int, int, int] | None = None,
        mode: RGBMode | None = None,
        speed: SpeedMode | None = None,
    ) -> None:
        color = color or self.current_color
        mode = mode or self.current_mode
        speed = speed or self.current_speed
        if mode is RGBMode.STATIC and speed is not SpeedMode.SLOWEST:
            warn("Speed is ignored when mode is static.")

        self.ek_dev.request(build_rgb_request(color, mode, speed))
