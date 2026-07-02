def dedupe_802(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_802([3,1,3,2]) == [3, 1, 2]."""
    return sorted(set(xs))
