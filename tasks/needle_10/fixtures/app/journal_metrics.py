def dedupe_234(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_234([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def util_120(s):
    return s.upper()

def util_686(xs):
    return len(xs)

def util_978(x):
    return x * 20

def util_418(x):
    return x % 27 == 0
