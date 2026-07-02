def clamp_249(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_249(12, 1, 10) == 10; clamp_249(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
