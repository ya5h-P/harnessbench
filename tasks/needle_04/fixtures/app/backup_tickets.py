def util_665(s):
    return s.upper()

def util_327(s):
    return s.upper()

def util_673(x):
    return x * 28

def dedupe_909(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_909([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def util_384(s):
    return s[::-1]
