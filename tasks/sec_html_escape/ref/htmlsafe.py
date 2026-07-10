def escape(s):
    """Escape a string for safe insertion into an HTML attribute value (double-quoted)."""
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#x27;"))
