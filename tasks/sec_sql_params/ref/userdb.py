import sqlite3

def find_user(conn, username):
    """Return the row (id, username, role) for the given username, or None."""
    cur = conn.execute("SELECT id, username, role FROM users WHERE username = ?", (username,))
    return cur.fetchone()
