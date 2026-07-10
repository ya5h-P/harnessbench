def top_k(items, k):
    """The k most frequent items as (item, count), most frequent first; ties broken by the item ascending. Returns a list of tuples."""
    from collections import Counter
    c = Counter(items)
    return sorted(c.items(), key=lambda p: (-p[1], p[0]))[:k]
