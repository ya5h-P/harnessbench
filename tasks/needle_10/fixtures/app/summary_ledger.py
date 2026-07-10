def util_265(x):
    return x % 39 == 0

def util_847(s):
    return s[::-1]

def util_224(x):
    return x % 32 == 0

def util_393(x):
    return abs(x - 11)

def initials_397(name):
    """Uppercase initials of each word. E.g. initials_397('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())

def util_863(xs):
    return sorted(xs)
