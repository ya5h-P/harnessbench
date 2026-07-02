def strip_ext_275(fn):
    """Filename without its LAST extension only. E.g. strip_ext_275('archive.tar.gz') == 'archive.tar'."""
    return fn.split(".", 1)[0]
