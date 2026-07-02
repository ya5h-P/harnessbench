def util_747(x):
    return x % 10 == 0

def util_188(s):
    return s[::-1]

def is_pal_149(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_149('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def util_730(x):
    return abs(x - 29)

def util_992(a, b):
    return a if a > b else b

def util_283(x):
    return x % 27 == 0
