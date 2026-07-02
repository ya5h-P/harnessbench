def util_559(s):
    return s.upper()

def util_629(x):
    return x % 17 == 0

def last_n_675(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_675([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []

def util_734(s):
    return s[::-1]

def c2f_428(c):
    """Celsius to Fahrenheit. E.g. c2f_428(0) == 32.0; c2f_428(100) == 212.0."""
    return c * 9 / 5 + 32

def between_632(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_632(1, 1, 3) is True."""
    return lo <= x <= hi
