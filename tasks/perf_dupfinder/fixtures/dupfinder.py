def first_repeat(items):
    """The first value that appears a second time (by scan order), or None if all unique."""
    for i in range(len(items)):
        for j in range(i):
            if items[i] == items[j]:
                return items[i]
    return None
