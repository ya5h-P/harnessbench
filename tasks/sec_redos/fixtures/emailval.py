import re

# BUG: this pattern has catastrophic backtracking on inputs like "aaaa...!" — a short
# malicious string makes matching take seconds (a ReDoS denial-of-service).
_EMAIL = re.compile(r"^(([a-zA-Z0-9]+)+)@example\.com$")

def is_valid_email(s):
    """True iff s is a <local>@example.com address (local part is alphanumeric)."""
    return _EMAIL.match(s) is not None
