def top_bigram(tokens):
    """The most frequent adjacent (tokens[i], tokens[i+1]) pair as a tuple; ties broken by the pair ascending. Returns None if fewer than 2 tokens."""
    if len(tokens) < 2:
        return None
    from collections import Counter
    c = Counter((tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1))
    return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
