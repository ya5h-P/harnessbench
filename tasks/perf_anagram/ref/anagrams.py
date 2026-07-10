def group_anagrams(words):
    """Group words that are anagrams. Returns groups sorted by their sorted-letter key; within each group words keep first-seen order."""
    from collections import OrderedDict
    d = OrderedDict()
    for w in words:
        d.setdefault(''.join(sorted(w)), []).append(w)
    return [d[k] for k in sorted(d)]
