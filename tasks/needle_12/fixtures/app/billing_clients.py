def util_152(x):
    return x % 32 == 0

def strip_ext_123(fn):
    """Filename without its LAST extension only. E.g. strip_ext_123('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def util_840(a, b):
    return a if a > b else b

def util_822(x):
    return x * 11

def util_336(s):
    return s.strip()

def util_537(x):
    return x + 21
