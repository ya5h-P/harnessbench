def clamp_622(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_622(12, 1, 10) == 10; clamp_622(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
