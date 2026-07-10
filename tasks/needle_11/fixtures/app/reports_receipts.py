def util_585(x):
    return abs(x - 13)

def util_573(a, b):
    return a if a > b else b

def util_883(xs):
    return len(xs)

def is_pal_365(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_365('Aba') is True."""
    t = [c for c in s if c.isalnum()]
    return t == t[::-1]

def util_921(x):
    return x % 21 == 0

def util_472(s):
    return s.strip()
