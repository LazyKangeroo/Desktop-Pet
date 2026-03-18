import random
import pyautogui
import sys

from enum import Enum

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer

# Screen dimensions
screen_width, screen_height = pyautogui.size()

class Directions(Enum):
    RIGHT = ['1.png', '2.png']
    LEFT = ['3.png', '4.png']

class Snail(QWidget):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Snail attributes
        self.sprite = 0
        self.count = 0

        # Label (create ONCE)
        self.label = QLabel(self)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(100)  # update every 100ms

    def animate(self):
        self.count += 1

        if self.count >= 5:
            self.count = 0
            self.sprite = 1 if self.sprite == 0 else 0

        img = Directions.RIGHT.value[self.sprite]
        self.updateSnail(img)

    def updateSnail(self, img):
        pixmap = QPixmap(img)

        self.label.setPixmap(pixmap)
        self.label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.resize(pixmap.width(), pixmap.height())


# RUN
if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = Snail()
    win.show()

    sys.exit(app.exec())