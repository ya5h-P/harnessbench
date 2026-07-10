def initials_157(name):
    """Uppercase initials of each word. E.g. initials_157('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
