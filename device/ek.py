import threading

import libusb_package
import usb.core

EK_VENDOR_ID = 0x0483
EK_PRODUCT_ID = 0x5750
EK_ENDPOINTS = [
    {
        "read": 0x81,
        "write": 0x01,
    },
    {
        "read": 0x82,
        "write": 0x02,
    },
]

BUFFER_SIZE = 63
REQ_TIMEOUT = 500


class EKDevice:
    def __init__(self) -> None:
        self.device: usb.core.Device = libusb_package.find(
            idVendor=EK_VENDOR_ID,
            idProduct=EK_PRODUCT_ID,
        )
        if self.device is None:
            raise ValueError("No EK device found")

        self.lock = threading.Lock()

    def _read(self, endpoint: int = 0) -> bytearray:
        data = self.device.read(
            EK_ENDPOINTS[endpoint]["read"],
            BUFFER_SIZE,
            timeout=REQ_TIMEOUT,
        )
        return data

    def _write(self, data: bytearray, endpoint: int = 0) -> None:
        self.device.write(EK_ENDPOINTS[endpoint]["write"], data)

    def request(self, request: bytearray, endpoint: int = 0) -> bytearray:
        with self.lock:
            self._write(request, endpoint)
            return self._read(endpoint)
