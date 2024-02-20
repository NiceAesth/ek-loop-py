from device.ek import EKDevice
from models.fan import FAN_COUNT
from models.fan import SpeedReadResponse
from models.fan import build_speed_read_request
from models.fan import build_speed_write_request


class FanService:
    """Service to interact with the fans and pumps on the EK Connect device. (Pump is fan 5)"""

    def __init__(self, ek_dev: EKDevice) -> None:
        self.ek_dev = ek_dev

    def get_connected_fan_count(self) -> int:
        """Returns the number of connected fans."""
        potential_fans = self.get_all_channels()
        return len([fan for fan in potential_fans if fan.rpm > 0])

    def get_fan_speed(self, channel: int) -> SpeedReadResponse:
        """Reads the speed of a fan.

        Args:
            channel (int): The channel to read the speed from. (0-5)
        """
        if channel < 0 or channel > 5:
            raise ValueError("Channel must be between 0 and 5")

        buffer = self.ek_dev.request(build_speed_read_request(channel))
        return SpeedReadResponse.from_buffer(channel, buffer)

    def get_all_channels(self) -> list[SpeedReadResponse]:
        """Reads the speed of all fans."""
        return [self.get_fan_speed(i) for i in range(FAN_COUNT)]

    def set_fan_speed(self, channel: int, pwm: int, rpm: int = 0) -> None:
        """Sets the speed of a fan.

        Args:
            channel (int): The channel to set the speed for. (0-5)
            pwm (int): The PWM value to set the fan to. (0-100%)
            rpm (int, optional): The RPM value to set the fan to. Defaults to 0.
        """
        if channel < 0 or channel > 5:
            raise ValueError("Channel must be between 0 and 5")
        if pwm < 0 or pwm > 100:
            raise ValueError("PWM value must be between 0 and 100")

        request = build_speed_write_request(channel, pwm, rpm)
        self.ek_dev.request(request)
