import functools
def retry(times):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*a, **k):
            last=None
            for _ in range(times):
                try: return fn(*a, **k)
                except Exception as e: last=e
            raise last
        return wrapper
    return deco
