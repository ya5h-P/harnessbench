def build_where(filters):
    if not filters:
        return "", []
    cols = sorted(filters)
    sql = " AND ".join("%s = ?" % c for c in cols)
    params = [filters[c] for c in cols]
    return sql, params
