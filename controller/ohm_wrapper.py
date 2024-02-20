# pyright: reportMissingImports=false
import clr

clr.AddReference("OpenHardwareMonitorLib")

from OpenHardwareMonitor.Hardware import Computer


class OHMWrapper:
    def __init__(self) -> None:
        self.computer = Computer()
        self.computer.CPUEnabled = True
        self.computer.GPUEnabled = True
        self.computer.Open()
        self.cpu_data = []
        self.gpu_data = []
        self.update_sensor_data()

    def update_sensor_data(self) -> None:
        for hardware in self.computer.Hardware:
            hardware.Update()
            if str(hardware.HardwareType) == "CPU":
                self.cpu_data.clear()
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) != "Temperature":
                        continue
                    self.cpu_data.append((sensor.Name, sensor.Value))
            if str(hardware.HardwareType) in ("GpuNvidia", "GpuAti"):
                self.gpu_data.clear()
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) != "Temperature":
                        continue
                    self.gpu_data.append((sensor.Name, sensor.Value))

    def get_cpu_temp(self) -> float:
        try:
            return self.cpu_data[-1][1]
        except IndexError:
            return 100.0

    def get_gpu_temp(self) -> float:
        try:
            return self.gpu_data[-1][1]
        except IndexError:
            return 100.0
