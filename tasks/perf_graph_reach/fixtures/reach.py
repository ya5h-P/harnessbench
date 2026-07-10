def reachable_count(n, edges, src):
    """Number of nodes reachable from src (including src) in a directed graph with nodes 0..n-1 and edges as (u, v) pairs."""
    reached = {src}
    changed = True
    while changed:
        changed = False
        for u, v in edges:
            if u in reached and v not in reached:
                reached.add(v); changed = True
    return len(reached)
