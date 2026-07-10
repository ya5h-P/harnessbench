def util_478(s):
    return s[::-1]

def util_506(a, b):
    return a if a > b else b

def util_929(x):
    return x * 26

def last_n_670(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_670([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []

def util_824(s):
    return s.strip()
