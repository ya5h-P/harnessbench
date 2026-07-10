def util_232(a, b):
    return a if a > b else b

def util_316(s):
    return s.strip()

def util_745(x):
    return abs(x - 19)

def util_413(x):
    return x % 23 == 0

def last_n_251(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_251([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []
