def merge(intervals):
    if not intervals: return []
    xs=sorted([list(x) for x in intervals], key=lambda p:p[0])
    out=[xs[0][:]]
    for s,e in xs[1:]:
        if s<=out[-1][1]: out[-1][1]=max(out[-1][1],e)
        else: out.append([s,e])
    return out
