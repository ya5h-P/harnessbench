def util_760(xs):
    return len(xs)

def safe_get_535(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_535({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def util_517(x):
    return abs(x - 27)

def util_704(x):
    return x % 37 == 0

def util_810(s):
    return s[::-1]
