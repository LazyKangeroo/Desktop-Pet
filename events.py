import time
import math
import threading
import win32gui
import win32con

import pyautogui as auto
from pynput.mouse import Listener
from PyQt6.QtGui import QCursor

EXCLUDED_WINDOW_TITLES = ['Pet', 'Settings', 'Windows Input Experience']

class MousePositioner:
    def __init__(self):
        pass

    def get_windows(self):
        windows = []

        def callback(hwnd, _):
            # Must be visible
            if not win32gui.IsWindowVisible(hwnd):
                return
            # Skip minimized
            if win32gui.IsIconic(hwnd):
                return
            title = win32gui.GetWindowText(hwnd)
            if not title.strip() or title in EXCLUDED_WINDOW_TITLES:
                return
            # Skip tool windows
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if style & win32con.WS_EX_TOOLWINDOW:
                return
            # Skip owned windows (not real app windows)
            if win32gui.GetWindow(hwnd, win32con.GW_OWNER):
                return
            # Must have size
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            if right - left == 0 or bottom - top == 0:
                return
            title = win32gui.GetWindowText(hwnd)
            if title: #? skips empty titles, usually system windows
                rect = win32gui.GetWindowRect(hwnd)
                windows.append({
                    "hwnd": hwnd,
                    "title": title,
                    "rect" : rect
                })

        win32gui.EnumWindows(callback, None)
        return windows

    def ontop_win(self):
        #? see whether curser is ontop of a window or on the desktop
        windows = self.get_windows()

        self.mouse_pos = QCursor.pos()

        for win in windows:
            print(win)
            print(self.mouse_pos)

            horz = False
            vert = False
            left, top, right, bottom = win['rect']
            x = self.mouse_pos.x()
            y = self.mouse_pos.y()

            if left <= x and right >= x:
                horz = True
            if top <= y and bottom >= y:
                vert = True
            if vert and horz:
                return True
        return False

    def get_icons(self):
        # get the positions of nearby icons to cursor
        pass

    def drag_icons(self):
        # used to drag nearby icons around
        pass

class MouseIdleDetector:
    def __init__(self, pet):
        """
        timeout: seconds before considered idle
        on_idle: function to call when idle
        """
        self.timeout = 3
        self.pet = pet

        self.last_activity_time = time.time()
        self.idle_triggered = False

        self._running = False
        self._thread = None
        self._listener = None

    def _on_mouse_event(self, *args):
        self.last_activity_time = time.time()
        self.idle_triggered = False
        return True

    def _monitor_idle(self):
        while self._running:
            time_passed = time.time() - self.last_activity_time
            if not self.idle_triggered:
                if time_passed > self.timeout:
                    action = self.pet.idle()
                    action()
                    self.idle_triggered = True
            # print(math.trunc(time_passed))
            time.sleep(0.5)

    def start(self):
        # Start detecting idle mouse"""
        self._running = True

        # Start background thread
        self._thread = threading.Thread(target=self._monitor_idle, daemon=True)
        self._thread.start()

        # Start mouse listener
        self._listener = Listener(
            on_move=self._on_mouse_event,
            on_click=self._on_mouse_event,
            on_scroll=self._on_mouse_event
        )
        self._listener.start()

        print('Detector started')

    def stop(self):
        # Stop detecting
        self._running = False
        if self._listener:
            self._listener.stop()