def clamp_351(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_351(12, 1, 10) == 10; clamp_351(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
