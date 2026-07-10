from urllib.parse import urlparse

ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}

def is_allowed(url):
    """True iff url is an http(s) URL whose host is in ALLOWED_HOSTS."""
    try:
        p = urlparse(url)
    except Exception:
        return False
    if p.scheme not in ("http", "https"):
        return False
    host = (p.hostname or "").lower().rstrip(".")
    return host in ALLOWED_HOSTS
