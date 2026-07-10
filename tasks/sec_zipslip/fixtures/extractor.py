import os, zipfile

def safe_extract(zip_path, dest):
    """Extract all members of the archive into dest/."""
    # BUG: trusts member names, so an entry like "../../evil.txt" escapes dest (Zip Slip).
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            target = os.path.join(dest, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(z.read(name))
