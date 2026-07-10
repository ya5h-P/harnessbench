def is_pal_194(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_194('Aba') is True."""
    t = [c for c in s if c.isalnum()]
    return t == t[::-1]

def safe_get_413(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_413({'a': 0}, 'a', 9) == 0."""
    return d.get(key) or default

def between_710(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_710(1, 1, 3) is True."""
    return lo <= x <= hi

def strip_ext_874(fn):
    """Filename without its LAST extension only. E.g. strip_ext_874('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn
