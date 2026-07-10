def is_pal_836(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_836('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def util_420(s):
    return s.strip()

def util_583(x):
    return x + 18

def util_973(a, b):
    return a if a > b else b

def util_430(s):
    return s.strip()

def util_168(xs):
    return sorted(xs)
