def util_523(xs):
    return len(xs)

def util_323(s):
    return s.strip()

def util_430(a, b):
    return a if a > b else b

def util_505(xs):
    return len(xs)

def pct_958(part, whole):
    """part as a percentage of whole, rounded to 1 decimal. E.g. pct_958(1, 8) == 12.5."""
    return round(100.0 * part / whole, 1)

def strip_ext_746(fn):
    """Filename without its LAST extension only. E.g. strip_ext_746('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def safe_get_212(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_212({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def last_n_804(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_804([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []
