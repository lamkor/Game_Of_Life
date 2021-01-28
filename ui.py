"""from PIL import Image
import numpy as np
import time
start = time.time()
im = Image.open('Untitled.png')
a = np.asarray(im)
im = Image.fromarray(a)
print(im.show())
print(time.time()-start)"""

import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
import pyautogui


def scale(old):
    new = int(window_width * (old / 800) * 0.8)
    return new


def font_scale(old_f):
    new_f = int(old_f * (window_height / 450) * 0.9)
    return new_f


mode, cell_size, alive, speed = '', '', '', ''  # Defining global variables
resolution = pyautogui.size()
window_width = int(resolution[0] * 0.8)
# window_width = 800
window_height = int(resolution[1] * 0.8)
# window_height = 450

canvas_width = window_width
canvas_height = window_height - scale(30)


class WindowClass(QWidget):
    def __init__(self, parent=None):
        super(WindowClass, self).__init__(parent)
        self.setWindowTitle('Game Of Life by Lamkor')
        self.resize(window_width, window_height)

        font1 = QtGui.QFont()
        font1.setFamily("Segoe UI")
        font1.setPointSize(font_scale(8))

        font2 = QtGui.QFont()
        font2.setFamily("Segoe UI")
        font2.setPointSize(font_scale(7))

        self.mode_label = QtWidgets.QLabel(self)
        self.mode_label.setGeometry(scale(6), scale(8), scale(33), scale(13))
        self.mode_label.setFont(font1)
        self.mode_label.setText('Mode:')

        self.game_mode = QtWidgets.QComboBox(self)
        self.game_mode.setGeometry(scale(45), scale(5), scale(67 + 10), scale(20))
        self.game_mode.setFont(font2)
        self.game_mode.addItem('With walls')
        self.game_mode.addItem('No walls')

        self.cell_size_label = QtWidgets.QLabel(self)
        self.cell_size_label.setGeometry(scale(130), scale(8), scale(51), scale(13))
        self.cell_size_label.setFont(font1)
        self.cell_size_label.setText('Cell Size:')

        self.cell_size_control = QtWidgets.QSpinBox(self)
        self.cell_size_control.setGeometry(scale(180), scale(5), scale(36), scale(20))
        self.cell_size_control.setFont(font2)

        self.alive_label = QtWidgets.QLabel(self)
        self.alive_label.setGeometry(scale(236), scale(8), scale(42), scale(13))
        self.alive_label.setFont(font1)
        self.alive_label.setText('Alive %:')

        self.alive_control = QtWidgets.QSpinBox(self)
        self.alive_control.setGeometry(scale(282), scale(5), scale(36), scale(20))
        self.alive_control.setFont(font2)

        self.speed_label = QtWidgets.QLabel(self)
        self.speed_label.setGeometry(scale(340), scale(8), scale(35), scale(13))
        self.speed_label.setFont(font1)
        self.speed_label.setText('Speed:')

        self.speed_control = QtWidgets.QSlider(self)
        self.speed_control.setGeometry(scale(382), scale(5 + 3), scale(127), scale(20 - 4))
        self.speed_control.setProperty('value', 20)
        self.speed_control.setOrientation(QtCore.Qt.Horizontal)

        self.start_button = QtWidgets.QPushButton(self)
        self.start_button.setGeometry(scale(730 * 1.27), scale(5), scale(65), scale(20))
        self.start_button.setFont(font1)
        self.start_button.setText('Start')
        self.start_button.clicked.connect(self.pressed)

        self.image_wrapper = QLabel(self)
        self.image_wrapper.setGeometry(scale(0), scale(30), canvas_width, canvas_height)
        self.image_wrapper.setPixmap(QPixmap(u"background.png"))
        self.image_wrapper.setScaledContents(True)

    def pressed(self):
        self.image_wrapper.setPixmap(QPixmap(u"Untitled.png"))
        n = self.start_button.text()
        if n == 'Start':
            global mode, cell_size, alive, speed
            # runtime started
            print("Program started")
            self.start_button.setText('Stop')
            mode = self.game_mode.currentText()
            cell_size = int(self.cell_size_control.text())
            alive = int(self.alive_control.text())
            speed = int(self.speed_control.value())
            print(mode, cell_size, alive, speed)

        else:
            # runtime stopped
            print("Program stopped")
            self.start_button.setText('Start')

    def event(self, e):
        if e.type() == QtCore.QEvent.MouseButtonPress:
            print("You clicked a mouse. Coordinates:", e.x(), e.y() - (window_height - canvas_height))
        '''        if e.type() == QtCore.QEvent.KeyPress:
            print("You pressed a button")
            print("Code:", e.key(), ", text:", e.text())
        elif e.type() == QtCore.QEvent.Close:
            print("You closed a window")'''
        return QWidget.event(self, e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wc = WindowClass()
    wc.show()
    sys.exit(app.exec_())
