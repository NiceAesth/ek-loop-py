from time import sleep
from typing import Literal

from fan_curve import BaseFanCurve
from ohm_wrapper import OHMWrapper
from pydantic import BaseModel

from ek_loop_py.device.ek import EKDevice
from ek_loop_py.services.fan import FanService
from ek_loop_py.services.sensor import SensorService


class BaseTempSource(BaseModel):
    controls: Literal[0, 1, 2, 3, 4, 5]


class ExternalTempSource(BaseTempSource):
    name: Literal["cpu", "gpu"]


class InternalTempSource(BaseTempSource):
    name: Literal["t1", "t2", "t3"]


TempSource = ExternalTempSource | InternalTempSource


class Config(BaseModel):
    fan_curve: BaseFanCurve
    temp_sources: list[TempSource]


class FanController:
    def __init__(self, ek_dev: EKDevice, config: Config) -> None:
        self.fan_service = FanService(ek_dev)
        self.sensor_service = SensorService(ek_dev)
        self.config = config
        self.sensor_data = self.sensor_service.get_sensor_data()
        self.fan_data = self.fan_service.get_all_channels()
        self.ohm_wrapper = OHMWrapper()

    def update_data(self) -> None:
        self.sensor_data = self.sensor_service.get_sensor_data()
        self.fan_data = self.fan_service.get_all_channels()
        self.ohm_wrapper.update_sensor_data()

    def update_fan_speed(self, channel_id: int, temp: float) -> None:
        pwm = int(self.config.fan_curve.get_pwm(temp))
        self.fan_service.set_fan_speed(channel_id, pwm)

    def print_sensor_data(self) -> None:
        print("\033[H\033[J", end="")
        print(
            f"T1: {self.sensor_data.t1_temp}°C, T2: {self.sensor_data.t2_temp}°C, T3: {self.sensor_data.t3_temp}°C",
        )
        print(
            f"CPU: {self.ohm_wrapper.get_cpu_temp()}°C, GPU: {self.ohm_wrapper.get_gpu_temp()}°C",
        )
        print(
            f"Flow: {self.sensor_data.flow} L/h, Coolant Status: {self.sensor_data.coolant_status.name}",
        )
        for fan in self.fan_data:
            if fan.rpm == 0:
                continue
            print(f"Fan {fan.channel}: {fan.rpm} RPM ({fan.pwm}%)")

    def loop(self) -> None:
        while True:
            self.print_sensor_data()
            for temp_source in self.config.temp_sources:
                if isinstance(temp_source, InternalTempSource):
                    temp = getattr(self.sensor_data, f"{temp_source.name}_temp")
                    self.update_fan_speed(temp_source.controls, temp)
                    continue
                if temp_source.name == "cpu":
                    temp = self.ohm_wrapper.get_cpu_temp()
                    self.update_fan_speed(temp_source.controls, temp)
                    continue
                if temp_source.name == "gpu":
                    temp = self.ohm_wrapper.get_gpu_temp()
                    self.update_fan_speed(temp_source.controls, temp)
                    continue
            sleep(5)
            self.update_data()
