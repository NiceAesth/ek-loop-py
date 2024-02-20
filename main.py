from contextlib import suppress
from time import sleep

from device.ek import EKDevice
from models.rgb import RGBMode as RGBM
from models.rgb import SpeedMode as SPM
from services.fan import FanService
from services.rgb import RGBService
from services.sensor import SensorService

ek_dev = EKDevice()
fan_service = FanService(ek_dev)
sensor_service = SensorService(ek_dev)
rgb_service = RGBService(ek_dev)


def main() -> None:
    rgb_service.set_rgb()

    while True:
        fan_data = fan_service.get_all_channels()
        sensor_data = sensor_service.read_sensor_data()
        print("\033[H\033[J", end="")
        print(
            f"T1: {sensor_data.t1_temp}°C, T2: {sensor_data.t2_temp}°C, T3: {sensor_data.t3_temp}°C",
        )
        print(
            f"Flow: {sensor_data.flow} L/h, Coolant Status: {sensor_data.coolant_status.name}",
        )
        for fan in fan_data:
            if fan.rpm == 0:
                continue
            print(f"Fan {fan.channel}: {fan.rpm} RPM ({fan.pwm}%)")
        sleep(1)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        main()
