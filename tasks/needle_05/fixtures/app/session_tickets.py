def util_658(x):
    return abs(x - 12)

def strip_ext_411(fn):
    """Filename without its LAST extension only. E.g. strip_ext_411('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def util_473(x):
    return x + 36

def util_117(x):
    return x + 12

def util_939(x):
    return abs(x - 21)
