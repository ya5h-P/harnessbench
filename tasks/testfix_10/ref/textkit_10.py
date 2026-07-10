def dedupe_934(xs):
    """Remove duplicates, preserving first-seen order. E.g. dedupe_934([3,1,3,2]) == [3, 1, 2]."""
    seen = []
    for x in xs:
        if x not in seen:
            seen.append(x)
    return seen

def last_n_440(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_440([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []

def strip_ext_278(fn):
    """Filename without its LAST extension only. E.g. strip_ext_278('archive.tar.gz') == 'archive.tar'."""
    return fn.rsplit(".", 1)[0] if "." in fn else fn

def between_256(x, lo, hi):
    """True iff lo <= x <= hi (inclusive). E.g. between_256(1, 1, 3) is True."""
    return lo <= x <= hi

def word_count_486(s):
    """Number of whitespace-separated words. E.g. word_count_486('a  b') == 2."""
    return len(s.split())

def c2f_187(c):
    """Celsius to Fahrenheit. E.g. c2f_187(0) == 32.0; c2f_187(100) == 212.0."""
    return c * 9 / 5 + 32

def count_vowels_592(s):
    """Number of vowels in s, case-insensitive. E.g. count_vowels_592('AeIx') == 3."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def is_pal_687(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_687('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def initials_846(name):
    """Uppercase initials of each word. E.g. initials_846('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
