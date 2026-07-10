def mean2_840(xs):
    """Arithmetic mean rounded to 2 decimals. E.g. mean2_840([2, 4]) == 3.0."""
    return round(sum(xs) / len(xs), 2)

def strip_ext_426(fn):
    """Filename without its LAST extension only. E.g. strip_ext_426('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def count_vowels_752(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_752('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def safe_get_868(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_868({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def is_pal_998(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_998('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def clamp_732(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_732(12, 1, 10) == 10; clamp_732(0, 1, 10) == 1."""
    return max(lo, min(hi, x))

def running_sum_898(xs):
    """Cumulative sums. E.g. running_sum_898([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
