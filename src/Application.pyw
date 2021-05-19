"""
Bryce Happel Walton
Ciena
5/18/2021
"""

from serial.tools.list_ports import comports
from module import SerialDevice, TkWindow, EZButton
from tkinter.ttk import Style, Frame, Button, Label, Combobox
from tkinter import StringVar

APPLICATION_TITLE = "PyDTMF"

X_FREQUENCIES = [1209, 1336, 1477, 1633]
Y_FREQUENCIES = [697, 770, 852, 941]

KEY_PAD = [
	[1, 2, 3, "A"],
	[4, 5, 6, "B"],
	[7, 8, 9, "C"],
	["*", 0, "#", "D"]
]

class DeviceSelection(TkWindow):
	"""
	A serial device selection prompt that will close itself upon selection
	"""

	def __init__(self):
		super().__init__("Device Select")
		self.value = StringVar()
		ports = comports()
		self._string_values = [
			f"{port.device}: {port.description}" for port in ports]
		self._real_values = [port.device for port in ports]
		self.selected_device = None

		self.selection_box = Combobox(
			self.frame, values=self._string_values, textvariable=self.value, state="readonly", width=40)
		self.selection_box.set("Select a device")
		self.selection_box.grid(row=0, column=0)
		self.selection_box.bind("<<ComboboxSelected>>", self._enable_confirm)

		self.buffer_frame = Frame(self.frame, height=8)
		self.buffer_frame.grid(row=1, column=0)

		self.confirm_button = Button(
			self.frame, text="Confirm", command=self._confirm, state="disabled")
		self.confirm_button.grid(row=2, column=0)
		super().mainloop()

	def _enable_confirm(self, event):
		"""
		Enables the confirmation button to select the device.
		> Called automagically when a device is selected in the combobox
		"""
		self.confirm_button.configure(state="enabled")

	def _confirm(self):
		"""
		destroys the application and sets the `selected_device` to be read from a third party
		> called automagically
		"""
		value = self.value.get()
		if value in self._string_values:
			self.selected_device = SerialDevice(
				self._real_values[self._string_values.index(value)], 128000)
			super().destroy()


class NoDeviceException(Exception):

	def __init__(self):
		super().__init__("No device selected")


class MainApplication(TkWindow):

	def __init__(self, title, device):
		if not device:
			raise NoDeviceException

		super().__init__(title)

		self.device = device
		self._build_keypad()
		self.device.write("start")
		self.protocol("WM_DELETE_WINDOW", self.quit)

	def write_freq_selection(self, x, y):
		self.device.write(f"{x}{y}")

	def button_down(self, x, y):
		return lambda event: self.write_freq_selection(x, y)

	def button_up(self, x, y):
		return lambda event: self.write_freq_selection(9, 9)

	def _build_keypad(self):
		unit_label = Label(self.frame, text="(Hz)")
		unit_label.grid(row=0, column=0)

		for x in range(len(X_FREQUENCIES)):
			label = Label(self.frame, text=X_FREQUENCIES[x])
			label.grid(row=0, column=x+1)

		for y in range(len(Y_FREQUENCIES)):
			label = Label(self.frame, text=Y_FREQUENCIES[y])
			label.grid(row=y+1, column=0)

		for y in range(len(KEY_PAD)):
			for x in range(len(KEY_PAD[y])):
				button = EZButton(self.frame, text=KEY_PAD[y][x])
				button.bind_button_down(self.button_down(x, y))
				button.bind_button_up(self.button_up(x, y))
				button.grid(row=y+1, column=x+1)

	def quit(self):
		self.device.write("stop")
		super().quit()

if __name__ == "__main__":
	device = DeviceSelection().selected_device
	MainApplication(APPLICATION_TITLE, device).mainloop()
