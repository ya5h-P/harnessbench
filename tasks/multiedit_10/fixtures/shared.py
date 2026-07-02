def limit_num(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. limit_num(12, 1, 10) == 10; limit_num(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
