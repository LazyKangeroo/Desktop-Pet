import math

from enum import Enum

from PyQt6.QtGui import QCursor

class Directions(Enum):
    RIGHT = ['sprites/cat/right_1.png', 'sprites/cat/right_2.png', 'sprites/cat/right_3.png', 'sprites/cat/right_4.png']
    LEFT = ['sprites/cat/left_1.png', 'sprites/cat/left_2.png','sprites/cat/left_3.png', 'sprites/cat/left_4.png']
    UP = ['sprites/cat/forward_1.png','sprites/cat/forward_2.png','sprites/cat/forward_3.png','sprites/cat/forward_4.png']
    DOWN = ['sprites/cat/back_1.png','sprites/cat/back_2.png','sprites/cat/back_3.png','sprites/cat/back_4.png']

SPRITE_SPEED = 2
STOPPING_DISTANCE = 5

class Cat:
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
                if self.sprite < 3:
                     self.sprite += 1
                else:
                    self.sprite = 0

            return self.sprite

        def update(self):
            ## Follow mouse
            self.mouse_pos = QCursor.pos()

            #? Get direction/distance of mouse
            self.geo = self.win.geometry() # This gets pos and size

            #* Calculate distance
            self.distanceX = self.mouse_pos.x() - self.geo.x() # if positive then move right, if negative then left
            self.distanceY = self.mouse_pos.y() - self.geo.y() # if positve then move down, if negative then move up
            distance = math.hypot(self.distanceX,self.distanceY)

            direction = self.get_direction()

            idle = False
            if distance < STOPPING_DISTANCE:
                idle = True
            else:
                speed = 10
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

        def get_direction(self):
            # since there are 4 different directional views I need to get an angle and see if the sprite is in a set angle range before changing directional sprite.
            # range between like 45-135 for up and down and the rest is left and right

            delta_x = self.mouse_pos.x() - self.geo.x()
            delta_y = self.mouse_pos.y() - self.geo.y()

            angle = math.atan2(delta_x, delta_y)
            angle = math.degrees(angle) # convert to usebale values

            if -45 <= angle <= 45:
                return Directions.UP
            elif 45 < angle <= 135:
                return Directions.RIGHT
            elif -135 <= angle < -45:
                return Directions.LEFT
            else:
                #? This covers the gap from 135 to 180 and -180 to -135
                return Directions.DOWN

        def idle(self):
            # this will take effect when the user doenst move the curser for a set amount of time, 2 minutes or so.
            # 3 things may happen
            # first if the cursor is on the desktop and near any icons the cat will move the icons arround. (no apps being used)
            # second an app is open the cat will start dragging around the cursor
            # thirdly this can happen whenever if the user is inactive enought, a random messge will be displayed in notepad by the cat
            #! Dragging cursor around
            action = self.dragging_mouse

            return action

        def dragging_mouse(self):
            print('Dragging mouse')