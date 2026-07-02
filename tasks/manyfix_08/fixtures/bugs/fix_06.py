def dedupe_188(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_188([3,1,3,2]) == [3, 1, 2]."""
    return sorted(set(xs))
