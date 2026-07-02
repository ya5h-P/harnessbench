def initials_646(name):
    """Uppercase initials of each word. E.g. initials_646('ada lovelace') == 'AL'."""
    return "".join(w[0] for w in name.split())
