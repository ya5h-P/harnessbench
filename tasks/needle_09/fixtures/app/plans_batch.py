def util_620(x):
    return abs(x - 9)

def strip_ext_714(fn):
    """Filename without its LAST extension only. E.g. strip_ext_714('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def util_441(s):
    return s[::-1]

def util_850(s):
    return s[::-1]
