def dedupe(items):
    """Remove duplicates, preserving order of first appearance. O(n)."""
    seen = set()
    result = []
    for x in items:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result
