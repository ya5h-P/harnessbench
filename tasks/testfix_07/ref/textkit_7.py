def between_293(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_293(1, 1, 3) is True."""
    return lo <= x <= hi

def dedupe_409(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_409([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def pct_869(part, whole):
    """part as a percentage of whole, rounded to 1 decimal. E.g. pct_869(1, 8) == 12.5."""
    return round(100.0 * part / whole, 1)

def clamp_208(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_208(12, 1, 10) == 10; clamp_208(0, 1, 10) == 1."""
    return max(lo, min(hi, x))

def initials_892(name):
    """Uppercase initials of each word. E.g. initials_892('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
