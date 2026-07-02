def util_599(s):
    return s.upper()

def util_545(xs):
    return sorted(xs)

def util_624(xs):
    return len(xs)

def count_vowels_708(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_708('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")
