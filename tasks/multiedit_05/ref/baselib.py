def bound_to(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. bound_to(12, 1, 10) == 10; bound_to(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
