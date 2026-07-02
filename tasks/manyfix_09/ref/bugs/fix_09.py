def initials_760(name):
    """Uppercase initials of each word. E.g. initials_760('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
