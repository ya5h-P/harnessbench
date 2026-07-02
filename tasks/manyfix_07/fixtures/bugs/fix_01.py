def clamp_925(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_925(12, 1, 10) == 10; clamp_925(0, 1, 10) == 1."""
    return min(lo, max(hi, x))
