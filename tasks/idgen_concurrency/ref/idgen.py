import time, threading
_state = {"n": 0}
_lock = threading.Lock()
def next_id():
    with _lock:
        v = _state["n"]
        time.sleep(0.000001)
        _state["n"] = v + 1
        return v
def reset():
    with _lock:
        _state["n"] = 0
