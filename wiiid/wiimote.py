import time
import serial
from PySide6.QtCore import QObject, QThread, Signal, Slot


class Wiimote(QThread):
    data = Signal(str)

    usb:serial.Serial
    def __init__(self):
        super().__init__()

    def do_work(self):
        self.usb = serial.Serial(port="/dev/cu.usbserial-0001", baudrate=115200)
        while True:
            read = self.usb.readline()
            if read:
                self.data.emit(str(read))
                print(read)

    def run(self):
        self.do_work()

    def disconnect(self):
        self.usb.close()
