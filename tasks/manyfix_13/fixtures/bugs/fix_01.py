def clamp_523(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_523(12, 1, 10) == 10; clamp_523(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
