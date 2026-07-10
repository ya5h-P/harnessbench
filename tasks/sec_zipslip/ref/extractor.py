import os, zipfile

def safe_extract(zip_path, dest):
    """Extract all members of the archive into dest/, refusing any path that escapes dest."""
    dest_abs = os.path.abspath(dest)
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            target = os.path.abspath(os.path.join(dest, name))
            if target != dest_abs and not target.startswith(dest_abs + os.sep):
                raise ValueError("unsafe path in archive: %s" % name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(z.read(name))
