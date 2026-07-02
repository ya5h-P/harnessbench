def clamp_909(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_909(12, 1, 10) == 10; clamp_909(0, 1, 10) == 1."""
    return max(lo, min(hi, x))

def is_pal_534(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_534('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def c2f_577(c):
    """Celsius to Fahrenheit. E.g. c2f_577(0) == 32.0; c2f_577(100) == 212.0."""
    return c * 9 / 5 + 32

def dedupe_972(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_972([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen
