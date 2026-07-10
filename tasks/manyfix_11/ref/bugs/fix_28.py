def strip_ext_829(fn):
    """Filename without its LAST extension only. E.g. strip_ext_829('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn
