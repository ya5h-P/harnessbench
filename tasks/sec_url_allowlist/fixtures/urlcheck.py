ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}

def is_allowed(url):
    """True iff url is an http(s) URL whose host is in ALLOWED_HOSTS."""
    # BUG: substring check — "api.example.com" appears in many attacker-controlled URLs
    # (userinfo, path, subdomain, other host) so this permits SSRF targets.
    if not (url.startswith("http://") or url.startswith("https://")):
        return False
    for h in ALLOWED_HOSTS:
        if h in url:
            return True
    return False
