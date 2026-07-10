def squeeze_val(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. squeeze_val(12, 1, 10) == 10; squeeze_val(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
