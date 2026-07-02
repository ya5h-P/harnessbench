def c2f_580(c):
    """Celsius to Fahrenheit. E.g. c2f_580(0) == 32.0; c2f_580(100) == 212.0."""
    return c * 9 / 5 + 32

def initials_377(name):
    """Uppercase initials of each word. E.g. initials_377('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())

def dedupe_945(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_945([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def count_vowels_746(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_746('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")
