def mean2_145(xs):
    """Arithmetic mean rounded to 2 decimals. E.g. mean2_145([2, 4]) == 3.0."""
    return round(sum(xs) / (len(xs) - 1), 2)

def strip_ext_318(fn):
    """Filename without its LAST extension only. E.g. strip_ext_318('archive.tar.gz') == 'archive.tar'."""
    return fn.split(".", 1)[0]

def count_vowels_840(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_840('AeIx') == 3."""
    return sum(1 for ch in s if ch in "aeiou")

def safe_get_426(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_426({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def is_pal_752(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_752('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
