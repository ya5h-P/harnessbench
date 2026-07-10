def clamp_507(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_507(12, 1, 10) == 10; clamp_507(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
