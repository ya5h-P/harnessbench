def util_791(x):
    return x + 14

def util_452(x):
    return abs(x - 15)

def util_549(x):
    return x % 12 == 0

def util_397(xs):
    return sorted(xs)

def pct_314(part, whole):
    """part as a percentage of whole, rounded to 1 decimal. E.g. pct_314(1, 8) == 12.5."""
    return round(100.0 * part / whole, 1)

def util_985(a, b):
    return a if a > b else b
