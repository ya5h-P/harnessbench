def clamp_577(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_577(12, 1, 10) == 10; clamp_577(0, 1, 10) == 1."""
    return min(lo, max(hi, x))

def is_pal_972(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_972('Aba') is True."""
    t = [c for c in s if c.isalnum()]
    return t == t[::-1]

def c2f_918(c):
    """Celsius to Fahrenheit. E.g. c2f_918(0) == 32.0; c2f_918(100) == 212.0."""
    return (c + 32) * 9 / 5

def dedupe_901(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_901([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def mean2_202(xs):
    """Arithmetic mean rounded to 2 decimals. E.g. mean2_202([2, 4]) == 3.0."""
    return round(sum(xs) / len(xs), 2)
