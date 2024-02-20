from contextlib import suppress

from fan_curve import *
from pyuac import main_requires_admin

from controller import Config
from controller import FanController
from ek_loop_py.device.ek import EKDevice

ek_dev = EKDevice()

with open("config.json") as f:
    config_json = f.read()

config = Config.parse_raw(config_json)


@main_requires_admin
def main() -> None:
    fan_controller = FanController(ek_dev, config=config)
    fan_controller.loop()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        main()
