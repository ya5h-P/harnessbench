def util_317(x):
    return abs(x - 28)

def util_172(xs):
    return len(xs)

def util_767(xs):
    return sorted(xs)

def util_547(x):
    return x * 22

def util_413(x):
    return x % 23 == 0

def initials_927(name):
    """Uppercase initials of each word. E.g. initials_927('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
