def safe_get_310(d, key, default):
    """d[key] if present else default; a stored falsy value is returned as-is. E.g. safe_get_310({'a': 0}, 'a', 9) == 0."""
    return d.get(key) or default

def strip_ext_237(fn):
    """Filename without its LAST extension only. E.g. strip_ext_237('archive.tar.gz') == 'archive.tar'."""
    return fn.split(".", 1)[0]

def clamp_276(x, lo, hi):
    """Clamp x into [lo, hi]. E.g. clamp_276(12, 1, 10) == 10; clamp_276(0, 1, 10) == 1."""
    return max(lo, min(hi, x))

def dedupe_225(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_225([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen
