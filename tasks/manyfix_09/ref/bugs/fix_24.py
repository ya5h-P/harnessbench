def running_sum_126(xs):
    """Cumulative sums. E.g. running_sum_126([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
