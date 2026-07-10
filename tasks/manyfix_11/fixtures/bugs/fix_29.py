def clamp_411(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_411(12, 1, 10) == 10; clamp_411(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
