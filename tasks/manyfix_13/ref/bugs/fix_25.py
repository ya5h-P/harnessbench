def is_pal_920(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_920('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
