def util_879(s):
    return s.upper()

def util_643(a, b):
    return a if a > b else b

def util_796(x):
    return x + 33

def util_695(a, b):
    return a if a > b else b

def safe_get_886(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_886({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def util_838(x):
    return x % 30 == 0
