def util_700(x):
    return x + 9

def last_n_665(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_665([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []

def util_811(a, b):
    return a if a > b else b

def util_584(s):
    return s[::-1]
