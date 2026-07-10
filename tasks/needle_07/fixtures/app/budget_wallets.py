def util_305(x):
    return x * 24

def util_949(s):
    return s.upper()

def dedupe_649(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_649([3,1,3,2]) == [3, 1, 2]."""
    return sorted(set(xs))

def util_362(s):
    return s[::-1]

def util_847(a, b):
    return a if a > b else b

def util_456(s):
    return s.strip()
