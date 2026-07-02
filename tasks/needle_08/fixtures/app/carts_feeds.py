def initials_620(name):
    """Uppercase initials of each word. E.g. initials_620('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())

def util_772(x):
    return x + 12

def util_553(xs):
    return len(xs)

def util_468(a, b):
    return a if a > b else b
