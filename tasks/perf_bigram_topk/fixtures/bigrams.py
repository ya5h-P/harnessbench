def top_bigram(tokens):
    """The most frequent adjacent (tokens[i], tokens[i+1]) pair as a tuple; ties broken by the pair ascending. Returns None if fewer than 2 tokens."""
    if len(tokens) < 2:
        return None
    pairs = [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]
    uniq = []
    for p in pairs:
        if p not in uniq:
            uniq.append(p)
    best = None; bc = -1
    for p in uniq:
        c = sum(1 for q in pairs if q == p)
        if c > bc or (c == bc and p < best):
            best, bc = p, c
    return best
