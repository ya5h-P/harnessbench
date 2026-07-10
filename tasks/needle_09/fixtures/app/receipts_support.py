def util_180(x):
    return x % 37 == 0

def is_pal_546(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_546('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def util_546(xs):
    return len(xs)

def util_336(a, b):
    return a if a > b else b

def util_105(xs):
    return len(xs)
