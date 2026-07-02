import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def read_doc(name):
    """Return the contents of a document, but only from inside the docs/ folder."""
    base = os.path.realpath(BASE)
    full = os.path.realpath(os.path.join(base, name))
    if full != base and not full.startswith(base + os.sep):
        raise ValueError("access denied: path escapes docs/")
    with open(full, encoding="utf-8") as f:
        return f.read()
