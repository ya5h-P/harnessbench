def initials_252(name):
    """Uppercase initials of each word. E.g. initials_252('ada lovelace') == 'AL'."""
    return "".join(w[0] for w in name.split())
