def util_457(x):
    return abs(x - 21)

def util_708(x):
    return x + 39

def util_221(a, b):
    return a if a > b else b

def util_637(s):
    return s[::-1]

def util_978(s):
    return s.strip()

def running_sum_410(xs):
    """Cumulative sums. E.g. running_sum_410([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
