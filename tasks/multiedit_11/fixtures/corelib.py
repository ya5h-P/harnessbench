def fit_range(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. fit_range(12, 1, 10) == 10; fit_range(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
