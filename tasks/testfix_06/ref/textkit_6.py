def safe_get_276(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_276({'a': 0}, 'a', 9) == 0."""
    return d.get(key, default)

def strip_ext_225(fn):
    """Filename without its LAST extension only. E.g. strip_ext_225('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def clamp_246(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_246(12, 1, 10) == 10; clamp_246(0, 1, 10) == 1."""
    return max(lo, min(hi, x))

def dedupe_717(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_717([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def pct_561(part, whole):
    """part as a percentage of whole, rounded to 1 decimal. E.g. pct_561(1, 8) == 12.5."""
    return round(100.0 * part / whole, 1)

def count_vowels_486(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_486('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")
