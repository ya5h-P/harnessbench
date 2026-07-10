def snap_to_range(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. snap_to_range(12, 1, 10) == 10; snap_to_range(0, 1, 10) == 1."""
    return max(lo, min(hi, x))
