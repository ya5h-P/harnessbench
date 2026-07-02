def dedupe(items):
    """Remove duplicates, preserving order of first appearance."""
    result = []
    for x in items:
        if x not in result:   # O(n) membership on a list -> O(n^2) overall
            result.append(x)
    return result
