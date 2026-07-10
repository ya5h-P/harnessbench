import os

UPLOAD_DIR = "uploads"

def save_upload(name, content):
    """Save content under UPLOAD_DIR/name and return the path written."""
    base = os.path.abspath(UPLOAD_DIR)
    path = os.path.abspath(os.path.join(base, name))
    if path != base and not path.startswith(base + os.sep):
        raise ValueError("path escapes upload directory: %s" % name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
