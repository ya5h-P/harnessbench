import re
_UNIT = {"h": 3600, "m": 60, "s": 1}
def parse_duration(s):
    if not s or not re.fullmatch(r"(\d+h)?(\d+m)?(\d+s)?", s) or s == "":
        raise ValueError("bad duration: %r" % s)
    total = 0; found = False
    for num, unit in re.findall(r"(\d+)([hms])", s):
        total += int(num) * _UNIT[unit]; found = True
    if not found:
        raise ValueError("empty duration")
    return total
def format_duration(n):
    if n == 0:
        return "0s"
    h, rem = divmod(n, 3600); m, s = divmod(rem, 60)
    out = ""
    if h: out += "%dh" % h
    if m: out += "%dm" % m
    if s: out += "%ds" % s
    return out
