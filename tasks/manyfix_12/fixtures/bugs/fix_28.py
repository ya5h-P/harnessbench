def strip_ext_616(fn):
    """Filename without its LAST extension only. E.g. strip_ext_616('archive.tar.gz') == 'archive.tar'."""
    return fn.split(".", 1)[0]
