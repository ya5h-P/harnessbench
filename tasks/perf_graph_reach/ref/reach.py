def reachable_count(n, edges, src):
    """Number of nodes reachable from src (including src) in a directed graph with nodes 0..n-1 and edges as (u, v) pairs."""
    from collections import defaultdict, deque
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
    seen = {src}; q = deque([src])
    while q:
        u = q.popleft()
        for v in g[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    return len(seen)
