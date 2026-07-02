def clamp_value(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_value(12, 1, 10) == 10; clamp_value(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
