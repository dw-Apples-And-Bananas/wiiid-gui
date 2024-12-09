import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from menu import Menu
from wiimote import Wiimote


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.wiimote = Wiimote()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    @QtCore.Slot()
    def connect_wiimote(self):
        self.wiimote.data.connect(self.text.setText)
        self.wiimote.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Window()
    widget.resize(800, 600)
    widget.show()

    Menu(widget).run()

    sys.exit(app.exec())
