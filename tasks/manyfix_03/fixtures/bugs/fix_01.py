def clamp_850(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_850(12, 1, 10) == 10; clamp_850(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
