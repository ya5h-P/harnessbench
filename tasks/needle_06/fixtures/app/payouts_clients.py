def util_815(xs):
    return sorted(xs)

def count_vowels_549(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_549('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def util_807(s):
    return s.strip()

def util_525(x):
    return x % 7 == 0
