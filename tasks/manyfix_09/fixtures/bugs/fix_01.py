def clamp_624(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_624(12, 1, 10) == 10; clamp_624(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
