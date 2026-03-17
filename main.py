import random
import pyautogui
import time

from enum import Enum

import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt

# Screen dimentions
screen_width, screen_height = pyautogui.size()

class Directions(Enum):
    RIGHT = ['1.png', '2.png']
    LEFT = ['3.png', '4.png']
    UP =  1
    DOWN = 2

# ENTITIES
class Human: # ?Mouse Cursor
    def __init__(self):
        pass

class Snail:
    def __init__(self):
        self.speed = 2
        self.pos = {
            'x' : random.randrange(0, screen_width),
            'y' : random.randrange(0, screen_height)
        }
        self.direction = "None"
        self.velocty = {
            'x' : 1,
            'y' : 1
        }

    def change_direction(self):
        pass

    def move(self):
        pass

    def update(self):
        pass

# WINDOW
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Makes window click through
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def display_img(self):
        label = QLabel(self)

        pixmap = QPixmap('1.png')

        label.setPixmap(pixmap)
        label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.resize(pixmap.width(), pixmap.height())

# RUN
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.display_img()
    win.show()
    sys.exit(app.exec())