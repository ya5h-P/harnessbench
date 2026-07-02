def util_879(s):
    return s.upper()

def util_643(a, b):
    return a if a > b else b

def util_796(x):
    return x + 33

def util_695(a, b):
    return a if a > b else b

def dedupe_886(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_886([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def util_838(x):
    return x % 30 == 0
