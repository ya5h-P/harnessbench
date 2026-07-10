def restrict_range(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. restrict_range(12, 1, 10) == 10; restrict_range(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
