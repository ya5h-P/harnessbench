def util_168(s):
    return s.strip()

def util_381(x):
    return x * 8

def util_910(s):
    return s.strip()

def util_588(x):
    return x * 31

def initials_432(name):
    """Uppercase initials of each word. E.g. initials_432('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
