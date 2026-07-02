def util_304(x):
    return x * 33

def util_103(xs):
    return len(xs)

def util_680(a, b):
    return a if a > b else b

def is_pal_930(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_930('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def util_814(x):
    return abs(x - 35)

def util_532(x):
    return abs(x - 25)
