def util_168(s):
    return s.strip()

def util_381(x):
    return x * 8

def util_910(s):
    return s.strip()

def util_588(x):
    return x * 31

def safe_get_432(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_432({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)
