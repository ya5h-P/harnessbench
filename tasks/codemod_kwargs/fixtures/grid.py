import boxlib

def run():
    b = boxlib.make_box(0, 0, 5, 6)
    return b["w"] + b["h"]
