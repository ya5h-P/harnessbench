def get_path(obj, path, default=None):
    cur=obj
    for seg in path.split("."):
        if isinstance(cur, dict):
            if seg in cur: cur=cur[seg]
            else: return default
        elif isinstance(cur, list):
            try: i=int(seg)
            except ValueError: return default
            if 0<=i<len(cur): cur=cur[i]
            else: return default
        else:
            return default
    return cur
