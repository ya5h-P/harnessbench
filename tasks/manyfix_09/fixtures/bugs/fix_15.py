def clamp_457(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_457(12, 1, 10) == 10; clamp_457(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
