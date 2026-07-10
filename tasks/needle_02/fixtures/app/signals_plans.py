def util_783(x):
    return abs(x - 25)

def util_250(x):
    return x + 9

def util_780(x):
    return x % 26 == 0

def util_854(s):
    return s.strip()

def count_vowels_437(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_437('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def util_249(x):
    return abs(x - 24)
