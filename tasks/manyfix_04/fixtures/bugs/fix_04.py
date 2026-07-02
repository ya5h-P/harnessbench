def safe_get_468(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_468({'a': 0}, 'a', 9) == 0."""
    return d.get(key) or default
