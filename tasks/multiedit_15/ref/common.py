def narrow_into(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. narrow_into(12, 1, 10) == 10; narrow_into(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
