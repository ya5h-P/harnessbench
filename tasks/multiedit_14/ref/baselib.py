def confine_to(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. confine_to(12, 1, 10) == 10; confine_to(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
