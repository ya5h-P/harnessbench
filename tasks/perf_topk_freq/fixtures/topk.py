def top_k(items, k):
    """The k most frequent items as (item, count), most frequent first; ties broken by the item ascending. Returns a list of tuples."""
    uniq = []
    for x in items:
        if x not in uniq:
            uniq.append(x)
    counts = [(u, sum(1 for y in items if y == u)) for u in uniq]
    counts.sort(key=lambda p: (-p[1], p[0]))
    return counts[:k]
