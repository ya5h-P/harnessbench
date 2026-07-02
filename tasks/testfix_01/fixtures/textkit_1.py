def strip_ext_355(fn):
    """Filename without its LAST extension only. E.g. strip_ext_355('archive.tar.gz') == 'archive.tar'."""
    return fn.split(".", 1)[0]

def is_pal_650(s):
    """True iff s is a palindrome ignoring case and non-alphanumerics. E.g. is_pal_650('Aba') is True."""
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]

def last_n_666(xs, n):
    """Last n items of xs (all of xs if n >= len). E.g. last_n_666([1,2,3,4], 2) == [3, 4]."""
    return list(xs[-n:]) if n > 0 else []
