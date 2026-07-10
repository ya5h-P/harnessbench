def util_295(x):
    return x + 24

def util_708(xs):
    return len(xs)

def strip_ext_243(fn):
    """Filename without its LAST extension only. E.g. strip_ext_243('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def util_964(s):
    return s.upper()
