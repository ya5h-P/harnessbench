def count_vowels_543(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_543('AeIx') == 3."""
    return sum(1 for ch in s if ch in "aeiou")
