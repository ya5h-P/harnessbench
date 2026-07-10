def initials_543(name):
    """Uppercase initials of each word. E.g. initials_543('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
