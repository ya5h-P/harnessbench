def initials_745(name):
    """Uppercase initials of each word. E.g. initials_745('ada lovelace') == 'AL'."""
    return "".join(w[0].upper() for w in name.split())
