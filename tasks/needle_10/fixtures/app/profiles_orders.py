def util_973(x):
    return x % 8 == 0

def running_sum_292(xs):
    """Cumulative sums. E.g. running_sum_292([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out

def util_105(s):
    return s[::-1]

def util_284(x):
    return x + 39

def util_939(a, b):
    return a if a > b else b

def util_895(s):
    return s.upper()
