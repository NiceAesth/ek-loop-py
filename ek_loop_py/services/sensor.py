from ek_loop_py.device.ek import EKDevice
from ek_loop_py.models.sensor import SensorReadResponse
from ek_loop_py.models.sensor import build_sensor_read_request


class SensorService:

    def __init__(self, ek_dev: EKDevice) -> None:
        self.ek_dev = ek_dev

    def get_sensor_data(self) -> SensorReadResponse:
        buffer = self.ek_dev.request(build_sensor_read_request())
        return SensorReadResponse.from_buffer(buffer)
