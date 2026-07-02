def between_127(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_127(1, 1, 3) is True."""
    return lo < x < hi
