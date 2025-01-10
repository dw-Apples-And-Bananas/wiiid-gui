from types import NoneType
from PySide6 import QtCore, QtWidgets, QtGui
import sys
import json
import os

from pynput.keyboard import Key, KeyCode, Controller

from menu import Menu
from wiimote import Wiimote

class Keyboard(Controller):
    def __init__(self) -> None:
        super().__init__()
    
    def tap(self, key: str | Key | KeyCode, mod: str | Key | KeyCode="") -> None:
        if mod != "":
            super().press(mod)
            super().tap(key)
            super().release(mod)
        else:
            super().tap(key)

    def press(self, key: str | Key | KeyCode, mod: str | Key | KeyCode="") -> None:
        if mod != "":
            super().press(mod)
            super().press(key)
            super().release(mod)
        else:
            super().press(key)

keyboard = Keyboard()

MAP = {
    "h": [["a"], 0, ""],
    "=": [["^"], 0, "cmd"],
    "-": [["v"], 0, "cmd"]
}

class WiimoteWidget:
    def __init__(self) -> None:
        scene = QtWidgets.QGraphicsScene()




        body_back_image = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("images/wiimote/body_back.png"))
        scene.addItem(body_back_image)

        self.unselected = {}
        for i in os.listdir("images/wiimote/unselected"):
            if i.endswith(".png"):
                btn = i.strip(".png")
                self.unselected[btn] = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(f"images/wiimote/unselected/{i}"))
                scene.addItem(self.unselected[btn])

        self.selected = {}
        for i in os.listdir("images/wiimote/selected"):
            if i.endswith(".png"):
                btn = i.strip(".png")
                self.selected[btn] = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(f"images/wiimote/selected/{i}"))
                self.selected[btn].setVisible(False)
                scene.addItem(self.selected[btn])

        body_front_image = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("images/wiimote/body_front.png"))
        scene.addItem(body_front_image)
        

        self.graphicsView = QtWidgets.QGraphicsView()

        self.graphicsView.setScene(scene)
        self.graphicsView.setStyleSheet("background: white;")
        # self.graphicsView.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("white")))



class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # APP UI
        self.setWindowTitle("WiiiD")
        pallete = self.palette()
        pallete.setColor(self.backgroundRole(), "#ffffff")
        self.setPalette(pallete)

        # UI
        self.wiimoteWidget = WiimoteWidget()
        layout = QtWidgets.QVBoxLayout()

        self.text = QtWidgets.QLabel("output", alignment=QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("color: #000000;")
        layout.addWidget(self.text)



        layout.addWidget(self.wiimoteWidget.graphicsView)

        self.setLayout(layout)

        # WIIMOTE
        self.wiimote = Wiimote()

    @QtCore.Slot()
    def connect_wiimote(self):
        self.wiimote.data.connect(self.process_wiimote_data)
        self.wiimote.start()

    def process_wiimote_data(self, data):
        data = json.loads(data)
        self.text.setText(str(data["a"]))
        for button in self.wiimoteWidget.selected.keys():
            if button in ["<", ">", "^", "v"]:
                unselected = self.wiimoteWidget.unselected["dpad"]
            else:
                unselected = self.wiimoteWidget.unselected[button]
            selected = self.wiimoteWidget.selected[button]
            if data[button] and not selected.isVisible():
                selected.setVisible(True)
                unselected.setVisible(False)
            elif not data[button] and selected.isVisible():
                selected.setVisible(False)
                unselected.setVisible(True)

        for key, value in MAP.items():
            btns = value[0]
            pressed = value[1]
            mod = value[2]
            for btn in btns:
                if data[btn] == 1 and not pressed:
                    MAP[key] = [btns, 1]
                    keyboard.press(key, mod)
                elif data[btn] == 0 and pressed:
                    MAP[key] = [btns, 0]
                    keyboard.release(key)

    
    def close(self):
        self.wiimote.quit()
        sys.exit()




if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Window()
    widget.resize(800, 600)
    widget.showMaximized()

    Menu(widget).run()

    sys.exit(app.exec())
