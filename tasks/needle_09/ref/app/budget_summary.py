def util_269(xs):
    return sorted(xs)

def running_sum_905(xs):
    """Cumulative sums. E.g. running_sum_905([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out

def util_448(x):
    return abs(x - 35)

def util_125(a, b):
    return a if a > b else b

def util_427(xs):
    return len(xs)
