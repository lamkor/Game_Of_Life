import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
import pyautogui
import numpy as np
import random
from PIL import Image
import time
import os
import res_1_rc


def scale(old):
    new = int(window_width * (old / 800) * 0.8)
    return new


def font_scale(old_f):
    new_f = int(old_f * (window_height / 450) * 0.9)
    return new_f


pixel = [2, 1, 46]
mode, cell_size, alive, speed = '', '', '', ''  # Defining global variables
resolution = pyautogui.size()
window_width = int(resolution[0] * 0.8)
window_height = int(resolution[1] * 0.8)

canvas_width = window_width
canvas_height = window_height - scale(30)
dism_width = 0
dism_height = 0


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
        self.cell_size_control.setMinimum(1)
        self.cell_size_control.setProperty('value', 10)

        self.alive_label = QtWidgets.QLabel(self)
        self.alive_label.setGeometry(scale(236), scale(8), scale(42), scale(13))
        self.alive_label.setFont(font1)
        self.alive_label.setText('Alive %:')

        self.alive_control = QtWidgets.QSpinBox(self)
        self.alive_control.setGeometry(scale(282), scale(5), scale(36), scale(20))
        self.alive_control.setFont(font2)
        self.alive_control.setProperty('value', 10)

        self.speed_label = QtWidgets.QLabel(self)
        self.speed_label.setGeometry(scale(340), scale(8), scale(35), scale(13))
        self.speed_label.setFont(font1)
        self.speed_label.setText('Speed:')

        self.speed_control = QtWidgets.QSlider(self)
        self.speed_control.setGeometry(scale(382), scale(5 + 3), scale(127), scale(20 - 4))
        self.speed_control.setProperty('value', 80)
        self.speed_control.setOrientation(QtCore.Qt.Horizontal)

        self.start_button = QtWidgets.QPushButton(self)
        self.start_button.setGeometry(scale(730 * 1.27), scale(5), scale(65), scale(20))
        self.start_button.setFont(font1)
        self.start_button.setText('Start')
        self.start_button.clicked.connect(self.pressed)

        self.background = QLabel(self)
        self.background.setGeometry(scale(0), scale(30), canvas_width, canvas_height)
        self.background.setPixmap(QPixmap(":imgs/background.png"))
        self.background.setScaledContents(True)

        self.image_wrapper = QLabel(self)
        self.image_wrapper.setGeometry(scale(0), scale(30), canvas_width, canvas_height)
        self.image_wrapper.setPixmap(QPixmap(":imgs/background.png"))
        self.image_wrapper.setScaledContents(True)

        self.dism_width = 0
        self.dism_height = 0


    def pressed(self):
        self.alive = 0
        n = self.start_button.text()
        if n == 'Start':
            global mode, cell_size, alive, speed
            # runtime started
            # print("Program started")
            self.start_button.setText('Stop')

            mode = self.game_mode.currentText()
            cell_size = int(self.cell_size_control.text())
            alive = int(self.alive_control.text())
            speed = 100 - int(self.speed_control.value())

            self.image_wrapper.setGeometry(scale(0) + int((canvas_width % cell_size) / 2),
                                           scale(30) + int((canvas_height % cell_size) / 2),
                                           canvas_width - int(canvas_width % cell_size),
                                           canvas_height - int(canvas_height % cell_size))
            self.image_wrapper.setPixmap(QPixmap(":imgs/background.png"))
            self.dism_width = self.image_wrapper.width()
            self.dism_height = self.image_wrapper.height()
            # print(mode, cell_size, alive, speed)
            self.runtime(mode, cell_size, alive, speed)

        else:
            # runtime stopped
            # print("Program stopped")
            self.start_button.setText('Start')
            sys.exit(app.exec_())
            file_path = 'temp.png'
            os.remove(file_path)

    def generate(self, field, alive):
        xmax, ymax = field.shape[0], field.shape[1]

        for x in range(xmax):
            for y in range(ymax):
                if random.random() <= int(alive) / 100:
                    field[x][y] = [255, 255, 255]
        return field

    def draw(self, field):
        field = np.repeat(np.repeat(field, cell_size, axis=1), cell_size, axis=0)
        im = Image.fromarray(field, 'RGB')
        im.save('temp.png')
        self.image_wrapper.setPixmap(QPixmap(u'temp.png'))

    def next_gen(self, field, mode):
        xmax, ymax = field.shape[0], field.shape[1]
        new_field = [[pixel for i in range(ymax)] for j in range(xmax)]
        new_field = np.asarray(new_field, dtype=np.uint8)
        for x in range(xmax):
            for y in range(ymax):
                n_count = self.check_neigh(field, x, y, mode)
                if field[x][y][0] == 255:
                    if n_count == 2 or n_count == 3:
                        new_field[x][y] = [255, 255, 255]
                    else:
                        new_field[x][y] = [2, 1, 46]
                else:
                    if n_count == 3:
                        new_field[x][y] = [255, 255, 255]
                    else:
                        new_field[x][y] = [2, 1, 46]
        return new_field

    def check_neigh(self, field, posx, posy, mode):
        xmax, ymax = field.shape[0], field.shape[1]
        neigh_count = 0
        if mode == 'No walls':
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    else:
                        try:
                            if field[posx + x][posy + y][0] == 255:
                                neigh_count += 1
                        except IndexError:
                            pass
        else:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0 or posx + x >= xmax or posx + x <= 0 or posy + y >= ymax or posy + y <= 0:
                        continue
                    else:
                        try:
                            if field[posx + x][posy + y][0] == 255:
                                neigh_count += 1
                        except IndexError:
                            pass

        return neigh_count

    def runtime(self, mode, cell_size, alive, speed):
        self.iter = 0
        self.mode = mode
        drawing_width = self.image_wrapper.width() // cell_size  # int(self.dism.width() / cell_size)
        drawing_height = self.image_wrapper.height() // cell_size  # int(self.dism.height() / cell_size)
        self.field = [[pixel for i in range(drawing_width)] for j in range(drawing_height)]
        self.field = np.asarray(self.field, dtype=np.uint8)
        self.field = self.generate(self.field, alive)

        def display():
            nonlocal mode, cell_size, alive, speed
            if self.iter == 0:
                self.draw(self.field)
                self.iter += 1
            else:
                self.field = self.next_gen(self.field, self.mode)
                self.draw(self.field)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(display)
        timer.start(speed * 50)

        # self.draw(field)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wc = WindowClass()
    wc.show()
    sys.exit(app.exec_())
