def is_pal_779(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_779('Aba') is True."""
    t = [c for c in s if c.isalnum()]
    return t == t[::-1]

def safe_get_194(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_194({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def between_413(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_413(1, 1, 3) is True."""
    return lo <= x <= hi
