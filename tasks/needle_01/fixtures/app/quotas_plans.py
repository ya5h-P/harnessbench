def util_392(a, b):
    return a if a > b else b

def util_340(a, b):
    return a if a > b else b

def util_944(a, b):
    return a if a > b else b

def util_930(s):
    return s.strip()

def safe_get_393(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_393({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def last_n_970(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_970([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []

def mean2_162(xs):
    """Arithmetic mean rounded to 2 decimals. E.g. mean2_162([2, 4]) == 3.0."""
    return round(sum(xs) / len(xs), 2)
