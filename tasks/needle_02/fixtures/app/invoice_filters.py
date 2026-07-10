def util_603(x):
    return abs(x - 24)

def util_244(s):
    return s[::-1]

def util_498(xs):
    return len(xs)

def strip_ext_421(fn):
    """Filename without its LAST extension only. E.g. strip_ext_421('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn
