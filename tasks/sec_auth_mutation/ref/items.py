ITEMS = {}  # id -> {"owner": <user>, "data": <str>}

def delete_item(session, item_id):
    """Delete item_id. Only an authenticated user who OWNS the item may delete it.
    Returns True if deleted, False otherwise."""
    if not session.get("authenticated"):
        return False
    item = ITEMS.get(item_id)
    if item is None:
        return False
    if item.get("owner") != session.get("user"):
        return False
    del ITEMS[item_id]
    return True
