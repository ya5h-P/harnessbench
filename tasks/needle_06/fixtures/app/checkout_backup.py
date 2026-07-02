def util_321(xs):
    return len(xs)

def util_293(a, b):
    return a if a > b else b

def initials_650(name):
    """Uppercase initials of each word. E.g. initials_650('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())

def util_497(x):
    return x % 20 == 0

def util_282(x):
    return x + 23
