def running_sum_339(xs):
    """Cumulative sums. E.g. running_sum_339([1, 2, 3]) == [1, 3, 6]."""
    total = 1
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
