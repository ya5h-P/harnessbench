def util_156(a, b):
    return a if a > b else b

def util_577(a, b):
    return a if a > b else b

def util_447(x):
    return x * 30

def is_pal_361(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_361('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
