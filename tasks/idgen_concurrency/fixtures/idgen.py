import time
_state = {"n": 0}
def next_id():
    v = _state["n"]
    time.sleep(0.000001)   # widens the race window
    _state["n"] = v + 1
    return v
def reset():
    _state["n"] = 0
