def util_233(x):
    return x % 37 == 0

def util_586(s):
    return s[::-1]

def util_124(s):
    return s.strip()

def util_917(a, b):
    return a if a > b else b

def word_count_108(s):
    """Number of whitespace-separated words. E.g. word_count_108('a  b') == 2."""
    return len(s.split(" "))
