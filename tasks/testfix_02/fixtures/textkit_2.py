def between_487(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_487(1, 1, 3) is True."""
    return lo < x < hi

def is_pal_367(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_367('Aba') is True."""
    t = [c for c in s if c.isalnum()]
    return t == t[::-1]

def pct_418(part, whole):
    """part as a percentage of whole, rounded to 1 decimal. E.g. pct_418(1, 8) == 12.5."""
    return round(100.0 * part / whole, 1)

def dedupe_560(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_560([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen
