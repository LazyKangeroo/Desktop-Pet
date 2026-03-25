import math

from enum import Enum

from PyQt6.QtGui import QCursor

class Directions(Enum):
    RIGHT = ['sprites/snail/1.png', 'sprites/snail/2.png']
    LEFT = ['sprites/snail/3.png', 'sprites/snail/4.png']

SPRITE_SPEED = 5
STOPPING_DISTANCE = 5

class Snail:
        def __init__(self, win):
            # Snail attributes
            self.sprite = 0
            self.count = 0

            #? Window object
            self.win = win

        def sprite_handle(self):
            self.count += 1

            if self.count >= SPRITE_SPEED:
                self.count = 0
                self.sprite = 1 if self.sprite == 0 else 0

            return self.sprite

        def update(self):
            ## Follow mouse
            mouse_pos = QCursor.pos()

            #? Get direction/distance of mouse
            self.geo = self.win.geometry() # This gets pos and size

            #* Calculate distance
            self.distanceX = mouse_pos.x() - self.geo.x() # if positive then move right, if negative then left
            self.distanceY = mouse_pos.y() - self.geo.y() # if positve then move down, if negative then move up
            distance = math.hypot(self.distanceX,self.distanceY)

            if self.distanceX < 0:
                 direction = Directions.LEFT
            else:
                 direction = Directions.RIGHT

            idle = False
            if distance < STOPPING_DISTANCE:
                idle = True
            else:
                speed = 5
                #  direction vector
                velocoityX = (self.distanceX / distance) * speed
                velocoityY = (self.distanceY / distance) * speed

                new_x = self.geo.x() + velocoityX
                new_y = self.geo.y() + velocoityY

            return {
                 'direction' : direction,
                 'x' : self.geo.x() if idle else new_x, # type: ignore
                 'y' : self.geo.y() if idle else new_y,  # type: ignore
                 'idle' : idle
            }

        def idle(self):
            return None