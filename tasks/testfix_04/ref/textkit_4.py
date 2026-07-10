def c2f_377(c):
    """Celsius to Fahrenheit. E.g. c2f_377(0) == 32.0; c2f_377(100) == 212.0."""
    return c * 9 / 5 + 32

def initials_945(name):
    """Uppercase initials of each word. E.g. initials_945('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())

def dedupe_746(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_746([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def count_vowels_392(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_392('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def strip_ext_401(fn):
    """Filename without its LAST extension only. E.g. strip_ext_401('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn
