def running_sum_936(xs):
    """Cumulative sums. E.g. running_sum_936([1, 2, 3]) == [1, 3, 6]."""
    total = 1
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
