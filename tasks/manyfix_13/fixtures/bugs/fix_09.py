def initials_352(name):
    """Uppercase initials of each word. E.g. initials_352('ada lovelace') == 'AL'."""
    return "".join(w[0] for w in name.split())
