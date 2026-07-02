def running_sum_457(xs):
    """Cumulative sums. E.g. running_sum_457([1, 2, 3]) == [1, 3, 6]."""
    total = 1
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
