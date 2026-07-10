ITEMS = {}  # id -> {"owner": <user>, "data": <str>}

def delete_item(session, item_id):
    """Delete item_id. Only an authenticated user who OWNS the item may delete it.
    Returns True if deleted, False otherwise."""
    # BUG: deletes first, and never checks authentication or ownership
    existed = item_id in ITEMS
    ITEMS.pop(item_id, None)
    return existed
