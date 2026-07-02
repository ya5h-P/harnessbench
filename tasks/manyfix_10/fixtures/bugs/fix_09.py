def initials_532(name):
    """Uppercase initials of each word. E.g. initials_532('ada lovelace') == 'AL'."""
    return "".join(w[0] for w in name.split())
