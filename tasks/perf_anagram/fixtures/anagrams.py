def group_anagrams(words):
    """Group words that are anagrams. Returns groups sorted by their sorted-letter key; within each group words keep first-seen order."""
    groups = []
    keys = []
    for w in words:
        k = sorted(w)
        placed = False
        for idx in range(len(keys)):
            if keys[idx] == k:
                groups[idx].append(w); placed = True; break
        if not placed:
            keys.append(k); groups.append([w])
    order = sorted(range(len(keys)), key=lambda i: keys[i])
    return [groups[i] for i in order]
