def escape(s):
    """Escape a string for safe insertion into an HTML attribute value (double-quoted)."""
    # BUG: escapes < and > but not & or the quote, so it does not neutralize
    # attribute-breaking payloads like  " onmouseover=alert(1)  or entity injection.
    return s.replace("<", "&lt;").replace(">", "&gt;")
