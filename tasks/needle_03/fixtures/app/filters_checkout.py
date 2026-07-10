def util_318(x):
    return abs(x - 26)

def count_vowels_484(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_484('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def util_655(x):
    return x % 18 == 0

def util_115(xs):
    return len(xs)
