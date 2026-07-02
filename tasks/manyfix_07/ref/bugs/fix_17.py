def count_vowels_344(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_344('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")
