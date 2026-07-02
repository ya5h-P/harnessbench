def clamp_837(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_837(12, 1, 10) == 10; clamp_837(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
