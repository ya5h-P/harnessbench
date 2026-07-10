def safe_get_944(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_944({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def is_pal_873(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_873('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def initials_133(name):
    """Uppercase initials of each word. E.g. initials_133('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())

def count_vowels_490(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_490('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def last_n_729(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_729([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []

def pct_274(part, whole):
    """part as a percentage of whole, rounded to 1 decimal. E.g. pct_274(1, 8) == 12.5."""
    return round(100.0 * part / whole, 1)

def between_443(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_443(1, 1, 3) is True."""
    return lo <= x <= hi

def dedupe_189(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_189([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def clamp_850(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_850(12, 1, 10) == 10; clamp_850(0, 1, 10) == 1."""
    return max(lo, min(hi, x))

def word_count_544(s):
    """Number of whitespace-separated words. E.g. word_count_544('a  b') == 2."""
    return len(s.split())

def strip_ext_832(fn):
    """Filename without its LAST extension only. E.g. strip_ext_832('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def running_sum_421(xs):
    """Cumulative sums. E.g. running_sum_421([1, 2, 3]) == [1, 3, 6]."""
    total = 0
    out = []
    for x in xs:
        total += x
        out.append(total)
    return out
