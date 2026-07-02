def parse_duration(s):
    # BUGGY: only understands minutes, no h/s, no validation
    num = ""
    for ch in s:
        if ch.isdigit():
            num += ch
    return int(num or 0) * 60

def format_duration(n):
    # BUGGY: only ever emits minutes
    return "%dm" % (n // 60)
