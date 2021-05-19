"""
Bryce Happel Walton
Ciena
5/18/2021
"""

from pyb import LED, USB_VCP, DAC
from pyb import millis, elapsed_millis, delay, Timer
from math import pi, sin
from array import array

INF = float("inf")

PWR_LED = LED(3)
DATA_LED = LED(4)

X_FREQUENCIES = [697, 770, 852, 941]
Y_FREQUENCIES = [1209, 1336, 1477, 1633]

x_buf = array("H", 2048 + int(2047 * sin(2 * pi * i / 128)) for i in range(128))
y_buf = array("H", 2048 + int(2047 * sin(2 * pi * i / 128)) for i in range(128))

x_dac = DAC(1, bits=12)
y_dac = DAC(2, bits=12)


class VCP(USB_VCP):

	def __init__(self):
		super().__init__()

	def read_timeout(self, timeout=5000):
		start_time = millis()
		while elapsed_millis(start_time) < timeout:
			data = self.read()
			if data:
				return data.decode()

	def write_encode(self, data):
		self.write(bytearray(str(data).encode()))

	def verify_write(self, data, timeout=500):
		timeout /= 2
		start_time = millis()
		while elapsed_millis(start_time) < timeout:
			self.write_encode(data)
			val = self.read_timeout(timeout)
			if val == str(data):
				return val

	def verify_read(self, timeout=500):
		data = self.read_timeout(timeout)
		self.write_encode(data)
		return data


def update_frequencies(x, y):
	if x == 9 or y == 9:
		x_dac.deinit()
		y_dac.deinit()
	else:
		x_freq = X_FREQUENCIES[y] * len(x_buf)
		y_freq = Y_FREQUENCIES[x] * len(y_buf)

		x_dac.write_timed(x_buf, Timer(8, freq=x_freq), mode=DAC.CIRCULAR)
		y_dac.write_timed(y_buf, Timer(7, freq=y_freq), mode=DAC.CIRCULAR)


def main():
	usb = VCP()

	while True:
		read = usb.read_timeout(INF)
		if read == "start":
			PWR_LED.on()
			while usb.isconnected():
				data = usb.read_timeout(INF)
				if data == "stop":
					update_frequencies(9, 9)
					PWR_LED.off()
					break
				else:
					x, y = int(data[0]), int(data[1])
					update_frequencies(x, y)


if __name__ == "__main__":
	main()
