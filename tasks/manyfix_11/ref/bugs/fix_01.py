def clamp_946(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_946(12, 1, 10) == 10; clamp_946(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
