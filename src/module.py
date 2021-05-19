"""
Bryce Happel Walton
Ciena
5/18/2021
"""
from time import time
from types import FunctionType
from threading import Thread
from serial import Serial
from tkinter import Tk
from tkinter.ttk import Frame, Button

import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def millis():
    """
    `return`: the milliseconds passed since epoch
    """
    return round(time() * 1000)


def elapsed_millis(start_time):
    """
    `start_time`: the beging time in milliseconds
    - recommended: millis()

    `return`: the time elapsed since `start_time`
    """
    return millis() - start_time


def min(table):
    """
    `table`: the table in which you want the minimum value from

    `return`: the minimum value in `table`
    """
    min = table[0]
    for i in table:
        if i < min:
            min = i
    return min


def max(table):
    """
    `table`: the table in which you want the maximum value from

    `return`: the maximum value in `table`
    """
    max = table[0]
    for i in table:
        if i > max:
            max = i
    return max


def spawn(function):
    """
    Will run `function` in a seperate thread

    `function`: the function being run in a seperate thread
    """
    Thread(target=function).start()


def int_input(text, fallback=None):
    """
    Will return an integer from user input. Will now allow user to input a string.
    Will allow the user to input nothing to fallback on a default value (fallback)

    `text`: the text that will be presented to the user via input(text)
    `fallback`: default value that will be returned if the user does not input anything

    `return`: int or `fallback`
    """
    while True:
        text = input(text)
        if not text and fallback:
            return fallback
        try:
            return int(text)
        except ValueError:
            print("Must be an integer!")


def float_input(text, fallback=None):
    """
    Will return a float from user input. Will now allow user to input a string.
    Will allow the user to input nothing to fallback on a default value (fallback)

    `text`: the text that will be presented to the user via input(text)
    `fallback`: default value that will be returned if the user does not input anything

    `return`: float or `fallback`
    """
    while True:
        text = input(text)
        if not text and fallback:
            return fallback
        try:
            return float(text)
        except ValueError:
            print("Must be a number (float)!")


class Event:
    """
    An event system that will run a given amount functions when fired.

    `functions`: the functions that will be called when the event is fired
    """

    def __init__(self, *functions):
        self.functions = []
        for func in functions:
            self.connect(func)

    def __len__(self):
        return len(self.functions)

    def __contains__(self, function):
        if function in self.functions:
            return True
        return False

    def fire(self, *args, **kwargs):
        """
        Calls the functions connected to the event when called.

        `args`: args for the functions
        `kwargs`: keyword args for the functions
        """
        for function in self.functions:
            # TODO: make a solution that doesn"t involve requiring each function to have args and kwargs
            function(args, kwargs)

    def connect(self, func):
        """
        Connects a function to the event to be called when the event is fired.

        `func`: function to add
        """
        if isinstance(func, FunctionType):
            self.functions.append(func)


class SerialDevice(Serial):
    """
    Sub-class of serial.Serial
    Specifically made to work around the buffer/encoded reads/writes

    `port`: the port of the COM device
    - Ex: `COM4`, `/dev/ttys4`, etc.

    `baudrate`: bits per second transfer-rate of the connection
    - Ex: `9600`, `19200`, `57600`
    """

    def __init__(self, port, baudrate=9600):
        super().__init__(port, baudrate)

    def kill(self):
        self.write("kill")
        super().close()

    def read_timeout(self, timeout=500, bytes=None):
        """
        `bytes`: given number of bytes to read from serial buffer
        `timeout`: time, in milliseconds, alloted before returning none if no data is read
        """
        start_time = millis()
        while elapsed_millis(start_time) < timeout:
            if super().in_waiting:
                data = super().read(bytes or super().in_waiting)
                if data:
                    return data.decode()

    def readline(self):
        """
        `return`: all bits in buffer until `\\n`
        - decodes, and removes `\\n`
        """
        return super().readline().decode()[:-1]

    def write(self, data):
        """
        `data`: data to write to the device
        """
        super().write(str(data).encode())

    def verify_write(self, data, timeout=500):
        """
        Will write to the device, and wait for the device to return that same value

        `data`: data to write to the device
        `timeout`: time, in milliseconds, alloted before returning none if no data is read
        """
        timeout /= 2
        start_time = millis()
        while elapsed_millis(start_time) < timeout:
            self.write(data)
            val = self.read_timeout(timeout)
            if val == str(data):
                return val

    def verify_read(self, timeout=500):
        """
        Will read from the device, and return that read value back to the device

        `timeout`: time, in milliseconds, alloted before returning none if no data is read
        """
        data = self.read_timeout(timeout)
        self.write(data)
        return data


class TkWindow(Tk):
    """
    Makes a Tk window

    `title`: the title of the window
    """

    def __init__(self, title):
        super().__init__()
        super().title(title)

        self.frame = Frame(self)
        self.frame.grid(sticky=("n", "e", "s", "w"), padx=8, pady=8)
        self._widgets = []

    def quit(self):
        super().quit()


class EZButton(Button):
    """
    More intuitive button class for button bindings
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def bind_button_down(self, callback):
        self.bind("<ButtonPress-1>", callback)

    def bind_button_up(self, callback):
        self.bind("<ButtonRelease-1>", callback)
