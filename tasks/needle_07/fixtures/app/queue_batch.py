def util_946(s):
    return s.upper()

def util_251(x):
    return abs(x - 5)

def util_544(s):
    return s.strip()

def util_614(s):
    return s.upper()

def util_266(xs):
    return len(xs)

def strip_ext_984(fn):
    """Filename without its LAST extension only. E.g. strip_ext_984('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn
