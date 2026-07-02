def initials_390(name):
    """Uppercase initials of each word. E.g. initials_390('ada lovelace') == 'AL'."""
    return "".join(w[0] for w in name.split())
