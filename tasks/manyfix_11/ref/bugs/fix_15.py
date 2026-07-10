def clamp_167(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_167(12, 1, 10) == 10; clamp_167(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
