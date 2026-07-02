import heapq
def shortest_distance(graph, start, end):
    dist={start:0}
    pq=[(0,start)]
    while pq:
        d,u=heapq.heappop(pq)
        if u==end: return d
        if d>dist.get(u,float("inf")): continue
        for v,w in graph.get(u,{}).items():
            nd=d+w
            if nd<dist.get(v,float("inf")):
                dist[v]=nd; heapq.heappush(pq,(nd,v))
    return dist.get(end, float("inf"))
