def apply_bounds(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. apply_bounds(12, 1, 10) == 10; apply_bounds(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
