def util_399(s):
    return s[::-1]

def util_300(s):
    return s.strip()

def util_379(x):
    return x * 39

def util_388(s):
    return s.strip()

def dedupe_491(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_491([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def mean2_327(xs):
    """Arithmetic mean rounded to 2 decimals. E.g. mean2_327([2, 4]) == 3.0."""
    return round(sum(xs) / len(xs), 2)

def initials_404(name):
    """Uppercase initials of each word. E.g. initials_404('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())

def last_n_879(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_879([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []

def running_sum_318(xs):
    """Cumulative sums. E.g. running_sum_318([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
