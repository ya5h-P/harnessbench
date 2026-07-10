def hold_between(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. hold_between(12, 1, 10) == 10; hold_between(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
