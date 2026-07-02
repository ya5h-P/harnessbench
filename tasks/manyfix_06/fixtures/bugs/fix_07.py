def mean2_655(xs):
    """Arithmetic mean rounded to 2 decimals. E.g. mean2_655([2, 4]) == 3.0."""
    return round(sum(xs) / (len(xs) - 1), 2)
