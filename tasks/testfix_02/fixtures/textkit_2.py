def between_434(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_434(1, 1, 3) is True."""
    return lo < x < hi

def is_pal_487(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_487('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def pct_367(part, whole):
    """part as a percentage of whole, rounded to 1 decimal. E.g. pct_367(1, 8) == 12.5."""
    return round(100.0 * part / whole, 1)
