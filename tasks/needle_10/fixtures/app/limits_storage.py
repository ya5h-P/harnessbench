def util_112(s):
    return s[::-1]

def util_343(x):
    return x % 34 == 0

def util_574(x):
    return x + 22

def util_510(x):
    return x * 31

def safe_get_391(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_391({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)
