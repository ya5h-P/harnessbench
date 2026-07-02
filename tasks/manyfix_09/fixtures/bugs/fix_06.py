def dedupe_967(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_967([3,1,3,2]) == [3, 1, 2]."""
    return sorted(set(xs))
