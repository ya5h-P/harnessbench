def util_580(x):
    return x % 38 == 0

def util_386(s):
    return s[::-1]

def running_sum_167(xs):
    """Cumulative sums. E.g. running_sum_167([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out

def util_319(xs):
    return len(xs)
