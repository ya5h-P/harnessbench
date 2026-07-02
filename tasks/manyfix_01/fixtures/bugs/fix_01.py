def clamp_274(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_274(12, 1, 10) == 10; clamp_274(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
