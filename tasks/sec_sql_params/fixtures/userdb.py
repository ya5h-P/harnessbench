import sqlite3

def find_user(conn, username):
    """Return the row (id, username, role) for the given username, or None."""
    # BUG: the value is inlined into SQL -> classic injection
    cur = conn.execute("SELECT id, username, role FROM users WHERE username = '%s'" % username)
    return cur.fetchone()
