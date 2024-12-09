import rumps
from PySide6.QtWidgets import QWidget


class Menu(rumps.App):
    def __init__(self, window:QWidget):
        super(Menu, self).__init__("[ WIIID ]")
        self.window = window
        self.menu = ["Show", "Connect", "Disconnect"]

    @rumps.clicked("Show")
    def show(self, _):
        self.window.show()
        self.window.raise_()

    @rumps.clicked("Connect")
    def connect(self, _):
        self.window.connect_wiimote()

    @rumps.clicked("Disconnect")
    def disconnect(self, _):
        self.window.wiimote.disconnect()
