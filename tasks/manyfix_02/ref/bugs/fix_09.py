def initials_412(name):
    """Uppercase initials of each word. E.g. initials_412('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
