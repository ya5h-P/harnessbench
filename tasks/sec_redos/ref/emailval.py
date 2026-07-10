import re

# a linear pattern: no nested quantifier over the same class, so no catastrophic backtracking
_EMAIL = re.compile(r"^[a-zA-Z0-9]+@example\.com$")

def is_valid_email(s):
    """True iff s is a <local>@example.com address (local part is alphanumeric)."""
    return _EMAIL.match(s) is not None
