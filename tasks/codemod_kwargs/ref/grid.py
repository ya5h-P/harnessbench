import boxlib

def run():
    b = boxlib.make_box(x=0, y=0, w=5, h=6)
    return b["w"] + b["h"]
