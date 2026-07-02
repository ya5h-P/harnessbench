def clamp_453(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_453(12, 1, 10) == 10; clamp_453(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
