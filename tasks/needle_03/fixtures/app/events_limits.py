def util_875(xs):
    return len(xs)

def util_842(s):
    return s[::-1]

def clamp_575(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_575(12, 1, 10) == 10; clamp_575(0, 1, 10) == 1."""
    return max(lo, min(hi, x))

def util_824(x):
    return x * 36
