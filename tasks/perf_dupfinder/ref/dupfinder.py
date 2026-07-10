def first_repeat(items):
    """The first value that appears a second time (by scan order), or None if all unique."""
    seen = set()
    for x in items:
        if x in seen:
            return x
        seen.add(x)
    return None
