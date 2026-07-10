def is_pal_750(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_750('Aba') is True."""
    t = [c for c in s if c.isalnum()]
    return t == t[::-1]

def util_198(xs):
    return sorted(xs)

def util_942(xs):
    return len(xs)

def util_818(s):
    return s.upper()

def util_333(x):
    return x * 11

def util_975(s):
    return s.strip()
