def update_user(user, data, allowed):
    """Apply only the fields named in `allowed` from dict `data` onto dict `user`."""
    # BUG: applies every key in data, ignoring `allowed` — a request body can set
    # privileged fields like is_admin or balance (mass-assignment / over-posting).
    user.update(data)
    return user
