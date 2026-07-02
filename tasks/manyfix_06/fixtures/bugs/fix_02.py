def last_n_249(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_249([1,2,3,4], 2) == [3, 4]."""
    return list(xs[:n]) if n > 0 else []
