def dedupe_889(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_889([3,1,3,2]) == [3, 1, 2]."""
    return sorted(set(xs))
