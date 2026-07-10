def util_875(xs):
    return len(xs)

def util_842(s):
    return s[::-1]

def running_sum_575(xs):
    """Cumulative sums. E.g. running_sum_575([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out

def util_824(x):
    return x * 36
