def max_overlap(intervals):
    """The maximum number of intervals (given as (start, end), end exclusive) that overlap at any single point."""
    points = set()
    for s, e in intervals:
        points.add(s)
    best = 0
    for p in points:
        c = sum(1 for s, e in intervals if s <= p < e)
        if c > best:
            best = c
    return best
