def clamp_474(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_474(12, 1, 10) == 10; clamp_474(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
