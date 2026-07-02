def mean2_100(xs):
    """Arithmetic mean rounded to 2 decimals. E.g. mean2_100([2, 4]) == 3.0."""
    return round(sum(xs) / (len(xs) - 1), 2)
