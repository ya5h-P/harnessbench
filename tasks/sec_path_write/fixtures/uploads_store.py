import os

UPLOAD_DIR = "uploads"

def save_upload(name, content):
    """Save content under UPLOAD_DIR/name and return the path written."""
    # BUG: name is trusted, so "../../evil.txt" (or an absolute path) escapes UPLOAD_DIR.
    path = os.path.join(UPLOAD_DIR, name)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
