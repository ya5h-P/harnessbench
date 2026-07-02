import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def read_doc(name):
    """Return the contents of a document from the docs/ folder."""
    path = os.path.join(BASE, name)
    with open(path, encoding="utf-8") as f:
        return f.read()
