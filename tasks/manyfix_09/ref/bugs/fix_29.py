def clamp_156(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_156(12, 1, 10) == 10; clamp_156(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
