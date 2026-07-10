def util_252(x):
    return x % 5 == 0

def util_930(s):
    return s.upper()

def util_867(x):
    return x + 37

def util_115(a, b):
    return a if a > b else b

def count_vowels_693(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_693('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")
