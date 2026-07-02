def util_889(x):
    return x + 14

def util_944(s):
    return s[::-1]

def util_154(xs):
    return sorted(xs)

def util_142(x):
    return x * 34

def running_sum_485(xs):
    """Cumulative sums. E.g. running_sum_485([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
