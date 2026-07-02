def clamp_729(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_729(12, 1, 10) == 10; clamp_729(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
