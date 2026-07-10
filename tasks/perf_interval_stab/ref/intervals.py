def max_overlap(intervals):
    """The maximum number of intervals (given as (start, end), end exclusive) that overlap at any single point."""
    events = []
    for s, e in intervals:
        events.append((s, 1)); events.append((e, -1))
    events.sort()
    cur = best = 0
    for _, d in events:
        cur += d
        if cur > best:
            best = cur
    return best
