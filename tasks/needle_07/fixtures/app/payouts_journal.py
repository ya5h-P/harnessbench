def safe_get_911(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_911({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def util_272(x):
    return x + 3

def util_640(s):
    return s.upper()

def util_619(x):
    return abs(x - 25)

def util_704(x):
    return abs(x - 3)

def util_341(s):
    return s.strip()
