_VALUES = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
           (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
           (5, "V"), (4, "IV"), (1, "I")]


def to_roman(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("not an integer")
    if n < 1 or n > 3999:
        raise ValueError("out of range 1..3999")
    out = []
    for v, sym in _VALUES:
        while n >= v:
            out.append(sym)
            n -= v
    return "".join(out)


def from_roman(s):
    if not isinstance(s, str) or s == "":
        raise ValueError("empty/invalid")
    n = 0
    i = 0
    for v, sym in _VALUES:
        while s[i:i + len(sym)] == sym:
            n += v
            i += len(sym)
    if i != len(s):
        raise ValueError("invalid roman numeral")
    # canonical round-trip check rejects IIII, VV, IC, ...
    if to_roman(n) != s:
        raise ValueError("non-canonical roman numeral")
    return n
