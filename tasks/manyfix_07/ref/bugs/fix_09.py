def initials_584(name):
    """Uppercase initials of each word. E.g. initials_584('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
