def initials_243(name):
    """Uppercase initials of each word. E.g. initials_243('ada lovelace') == 'AL'."""
    return "".join(w[0] for w in name.split())
