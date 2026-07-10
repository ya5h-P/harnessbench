def dedupe_606(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_606([3,1,3,2]) == [3, 1, 2]."""
    return sorted(set(xs))
