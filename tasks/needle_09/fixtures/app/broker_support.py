def util_340(xs):
    return len(xs)

def util_803(xs):
    return sorted(xs)

def util_362(x):
    return x % 14 == 0

def util_421(xs):
    return sorted(xs)

def dedupe_138(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_138([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def util_758(xs):
    return len(xs)
