def clamp_386(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_386(12, 1, 10) == 10; clamp_386(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
