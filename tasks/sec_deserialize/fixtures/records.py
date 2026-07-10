import pickle, base64

def load_record(blob):
    """Decode a base64 record produced by the client and return the dict."""
    # BUG: pickle executes arbitrary code on load — an attacker-crafted blob runs code.
    return pickle.loads(base64.b64decode(blob))
