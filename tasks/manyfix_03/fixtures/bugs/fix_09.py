def initials_989(name):
    """Uppercase initials of each word. E.g. initials_989('ada lovelace') == 'AL'."""
    return "".join(w[0] for w in name.split())
