def clamp_543(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_543(12, 1, 10) == 10; clamp_543(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
