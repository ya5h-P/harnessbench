def update_user(user, data, allowed):
    """Apply only the fields named in `allowed` from dict `data` onto dict `user`."""
    for k in allowed:
        if k in data:
            user[k] = data[k]
    return user
