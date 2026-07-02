def keep_within(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. keep_within(12, 1, 10) == 10; keep_within(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
