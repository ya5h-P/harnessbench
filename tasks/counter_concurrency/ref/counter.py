import time
import threading


class Counter:
    def __init__(self):
        self._v = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            tmp = self._v
            time.sleep(0.000001)
            self._v = tmp + 1

    @property
    def value(self):
        with self._lock:
            return self._v
