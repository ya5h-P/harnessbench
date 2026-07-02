def util_606(s):
    return s[::-1]

def util_782(x):
    return abs(x - 30)

def util_634(x):
    return x * 2

def count_vowels_195(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_195('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def util_374(a, b):
    return a if a > b else b
