# ek-loop-py

## Description

This is a Python script that interacts with the EK-Loop Connect fan controller. The motivation behind this project is the abhorrent state of the official software.

Support for fan control, RGB control and sensor monitoring is offered.

## Installation

See the `Makefile`. This project targets Python 3.11+.

## Acknowledgements

pavelherr's [ek-loop-connect](https://github.com/pavelherr/ek-loop-connect) linux driver was invaluable in understanding the USB protocol behind the controller.
The RGB control code was based off of [OpenRGB's implementation](https://gitlab.com/CalcProgrammer1/OpenRGB/-/tree/master/Controllers/EKController).

## License

MIT. Do whatever you want, I am not responsible for anything.
