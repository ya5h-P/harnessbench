def clamp_425(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_425(12, 1, 10) == 10; clamp_425(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
