def strip_ext_556(fn):
    """Filename without its LAST extension only. E.g. strip_ext_556('archive.tar.gz') == 'archive.tar'."""
    return fn.split(".", 1)[0]
