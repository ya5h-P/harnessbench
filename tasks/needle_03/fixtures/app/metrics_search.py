def util_429(xs):
    return sorted(xs)

def util_126(x):
    return x + 21

def util_540(x):
    return x % 36 == 0

def safe_get_845(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_845({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)
