from device.ek import EKDevice
from models.sensor import SensorReadResponse
from models.sensor import build_read_request


class SensorService:

    def __init__(self, ek_dev: EKDevice) -> None:
        self.ek_dev = ek_dev

    def read_sensor_data(self):
        buffer = self.ek_dev.request(build_read_request())
        return SensorReadResponse.from_buffer(buffer)
