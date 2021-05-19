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

class MainApplication(TkWindow):

	def __init__(self, title):
		super().__init__(title)
		self._build_keypad()
		self.protocol("WM_DELETE_WINDOW", self.quit)

	def button_down(self, x, y):
		return lambda event: print(f"writing {x}{y}")

	def button_up(self, x, y):
		return lambda event: print(f"writing {9}{9}")

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
		print("Ending")
		super().quit()


if __name__ == "__main__":
	MainApplication(APPLICATION_TITLE).mainloop()
