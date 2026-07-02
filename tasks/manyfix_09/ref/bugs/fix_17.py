def count_vowels_438(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_438('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")
