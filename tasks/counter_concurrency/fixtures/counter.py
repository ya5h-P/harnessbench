import time


class Counter:
    def __init__(self):
        self._v = 0

    def increment(self):
        tmp = self._v
        time.sleep(0.000001)   # widens the read-modify-write race window
        self._v = tmp + 1

    @property
    def value(self):
        return self._v
