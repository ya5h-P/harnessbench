def coerce_span(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. coerce_span(12, 1, 10) == 10; coerce_span(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
