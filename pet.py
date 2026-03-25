import pyautogui
import sys

from snail import Snail
from cat import Cat

from events import MouseIdleDetector

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer, QPoint

# Screen dimensions
screen_width, screen_height = pyautogui.size()

#! Getting commandline arguement
# Determines the type of sprite used
arguement = (sys.argv[1]).lower()

class Main(QWidget):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle('Pet')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Point/Pos
        self.point = QPoint()

        # Label
        self.label = QLabel(self)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(100)  # update every 100ms
        self.timer_count = 0

        #! Type
        # will be dependend on input before hand
        match arguement:
            case 'snail':
                self.pet = Snail(self)
            case 'cat':
                self.pet = Cat(self)
            case _:
                print('No Sprite Type chosen')
                sys.exit()

        # Mouse detector
        if self.pet.idle() != None:
            self.detector = MouseIdleDetector(self.pet)
            self.detector.start()

    def animate(self):
        #! Cycle
        sprite = self.pet.sprite_handle()

        #? Updated Pos from pet class
        updatedPos = self.pet.update()

        if updatedPos['idle']:
            sprite = 0

        self.move(int(updatedPos['x']), int(updatedPos['y']))

        if updatedPos['direction'] is not None:
            img = updatedPos['direction'].value[sprite]
        else:
            return

        self.updateImg(img)

    def updateImg(self, img):
        pixmap = QPixmap(img)

        self.label.setPixmap(pixmap)
        self.label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.resize(pixmap.width(), pixmap.height())

# RUN
if __name__ == "__main__":
    #? App
    app = QApplication(sys.argv)

    win = Main()
    win.show()

    sys.exit(app.exec())