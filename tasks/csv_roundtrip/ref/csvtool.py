def parse(text):
    fields = []
    i, n = 0, len(text)
    while True:
        field = []
        if i < n and text[i] == '"':
            i += 1
            while i < n:
                c = text[i]
                if c == '"':
                    if i + 1 < n and text[i + 1] == '"':
                        field.append('"'); i += 2; continue
                    i += 1; break
                field.append(c); i += 1
        else:
            while i < n and text[i] != ',':
                field.append(text[i]); i += 1
        fields.append(''.join(field))
        if i < n and text[i] == ',':
            i += 1; continue
        break
    return fields


def dump(fields):
    out = []
    for f in fields:
        if ',' in f or '"' in f:
            out.append('"' + f.replace('"', '""') + '"')
        else:
            out.append(f)
    return ','.join(out)
