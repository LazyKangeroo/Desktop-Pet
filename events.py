import time
import threading
from pynput.mouse import Listener

class MouseIdleDetector:
    def __init__(self, timeout=5, on_idle=None):
        """
        timeout: seconds before considered idle
        on_idle: function to call when idle
        """
        self.timeout = timeout
        self.on_idle = on_idle or self.default_action

        self.last_activity_time = time.time()
        self.idle_triggered = False

        self._running = False
        self._thread = None
        self._listener = None

    def default_action(self):
        print(f"Move the darm mouse dont be boring.")

    def _on_mouse_event(self, *args):
        self.last_activity_time = time.time()
        self.idle_triggered = False
        return True

    def _monitor_idle(self):
        while self._running:
            time_passed = time.time() - self.last_activity_time
            if not self.idle_triggered:
                if time_passed > self.timeout:
                    self.on_idle()
                    self.idle_triggered = True
            print(time_passed)
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