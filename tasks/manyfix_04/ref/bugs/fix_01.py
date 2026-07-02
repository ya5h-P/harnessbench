def clamp_113(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_113(12, 1, 10) == 10; clamp_113(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
