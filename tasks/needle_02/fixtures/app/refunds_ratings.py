def safe_get_897(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_897({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def util_166(s):
    return s[::-1]

def util_467(xs):
    return sorted(xs)

def util_584(s):
    return s[::-1]

def util_857(xs):
    return len(xs)
