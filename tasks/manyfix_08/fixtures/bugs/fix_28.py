def strip_ext_262(fn):
    """Filename without its LAST extension only. E.g. strip_ext_262('archive.tar.gz') == 'archive.tar'."""
    return fn.split(".", 1)[0]
