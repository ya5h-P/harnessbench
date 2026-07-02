def clamp_868(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_868(12, 1, 10) == 10; clamp_868(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
