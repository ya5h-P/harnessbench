def is_pal_597(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_597('Aba') is True."""
    t = [c for c in s if c.isalnum()]
    return t == t[::-1]
