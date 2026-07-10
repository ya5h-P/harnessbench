def util_700(x):
    return x + 9

def safe_get_665(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_665({'a': 0}, 'a', 9) == 0."""
    return d.get(key) or default

def util_811(a, b):
    return a if a > b else b

def util_584(s):
    return s[::-1]
