def initials_167(name):
    """Uppercase initials of each word. E.g. initials_167('ada lovelace') == 'AL'."""
    return "".join(w[0] for w in name.split())
