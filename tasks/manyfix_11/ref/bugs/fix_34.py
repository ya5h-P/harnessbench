def dedupe_274(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_274([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen
