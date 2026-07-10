def make_box(*, x, y, w, h):
    """Return a box dict. Arguments are keyword-only."""
    return {"x": x, "y": y, "w": w, "h": h, "area": w * h}
