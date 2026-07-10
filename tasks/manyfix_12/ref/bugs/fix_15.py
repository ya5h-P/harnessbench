def clamp_429(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_429(12, 1, 10) == 10; clamp_429(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
