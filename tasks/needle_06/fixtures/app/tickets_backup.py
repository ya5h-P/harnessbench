def util_815(xs):
    return sorted(xs)

def safe_get_549(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_549({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def util_807(s):
    return s.strip()

def util_525(x):
    return x % 7 == 0
