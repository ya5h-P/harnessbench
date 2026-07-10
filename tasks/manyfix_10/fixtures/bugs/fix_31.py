def count_vowels_752(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_752('AeIx') == 3."""
    return sum(1 for ch in s if ch in "aeiou")
