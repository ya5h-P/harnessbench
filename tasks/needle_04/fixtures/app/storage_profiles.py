def util_706(s):
    return s.upper()

def util_393(xs):
    return len(xs)

def count_vowels_978(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_978('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def util_979(s):
    return s[::-1]
