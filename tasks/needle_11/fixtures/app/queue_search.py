def util_235(xs):
    return len(xs)

def strip_ext_709(fn):
    """Filename without its LAST extension only. E.g. strip_ext_709('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def util_745(s):
    return s.upper()

def util_308(s):
    return s.strip()
