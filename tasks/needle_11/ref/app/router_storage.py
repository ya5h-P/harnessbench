def util_135(x):
    return x * 24

def util_906(xs):
    return sorted(xs)

def util_646(x):
    return x + 10

def count_vowels_192(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_192('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def util_244(x):
    return abs(x - 2)
