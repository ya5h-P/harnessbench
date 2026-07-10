from baselib import confine_to

def run(x):
    return confine_to(x, 3, 31)
