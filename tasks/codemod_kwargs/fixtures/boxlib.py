def make_box(x, y, w, h):
    """Return a box dict. NOTE: being migrated to keyword-only arguments."""
    return {"x": x, "y": y, "w": w, "h": h, "area": w * h}
