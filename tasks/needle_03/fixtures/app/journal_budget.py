def util_149(x):
    return x % 4 == 0

def is_pal_552(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_552('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def util_923(a, b):
    return a if a > b else b

def util_324(x):
    return abs(x - 9)

def util_606(x):
    return x * 8

def util_570(x):
    return x * 15
