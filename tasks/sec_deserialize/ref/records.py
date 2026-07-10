import json, base64

def load_record(blob):
    """Decode a base64 record produced by the client and return the dict."""
    return json.loads(base64.b64decode(blob).decode("utf-8"))
