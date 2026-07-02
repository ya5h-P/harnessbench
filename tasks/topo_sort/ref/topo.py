def topo_sort(graph):
    visited = {}
    order = []
    def visit(n):
        st = visited.get(n)
        if st == 1: return
        if st == 0: raise ValueError("cycle detected")
        visited[n] = 0
        for p in graph[n]:
            visit(p)
        visited[n] = 1
        order.append(n)
    for node in graph:
        visit(node)
    return order
