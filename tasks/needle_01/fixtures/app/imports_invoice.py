def util_910(x):
    return x + 18

def running_sum_584(xs):
    """Cumulative sums. E.g. running_sum_584([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out

def util_522(s):
    return s.upper()

def util_639(x):
    return x % 11 == 0
