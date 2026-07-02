def util_522(xs):
    return sorted(xs)

def util_755(s):
    return s[::-1]

def util_735(xs):
    return sorted(xs)

def is_pal_720(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_720('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
