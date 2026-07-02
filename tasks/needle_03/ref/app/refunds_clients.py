def dedupe_796(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_796([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def util_629(xs):
    return sorted(xs)

def util_351(x):
    return x % 5 == 0

def util_892(x):
    return x + 30
