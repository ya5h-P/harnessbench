"""geometry toolkit — everything in one file (needs splitting)."""
import math

PI = 3.141592653589793


def area_circle(r):
    """Area of a circle of radius r."""
    return PI * r * r


def perimeter_circle(r):
    """Circumference of a circle of radius r."""
    return 2 * PI * r


def area_square(s):
    """Area of a square of side s."""
    return s * s


def perimeter_square(s):
    """Perimeter of a square of side s."""
    return 4 * s


def area_rect(w, h):
    """Area of a w x h rectangle."""
    return w * h


def perimeter_rect(w, h):
    """Perimeter of a w x h rectangle."""
    return 2 * (w + h)


def area_triangle(b, h):
    """Area of a triangle with base b and height h."""
    return 0.5 * b * h


def hypotenuse(a, b):
    """Hypotenuse of a right triangle with legs a and b."""
    return math.sqrt(a * a + b * b)


def describe(shape, *dims):
    """Return "<shape>: area=<a>, perimeter=<p>" for shape in
    {circle, square, rect, triangle}. Triangle reports perimeter as the sum of the
    two given legs plus the hypotenuse (a right triangle b, h)."""
    if shape == "circle":
        return "circle: area=%.4f, perimeter=%.4f" % (area_circle(dims[0]), perimeter_circle(dims[0]))
    if shape == "square":
        return "square: area=%.4f, perimeter=%.4f" % (area_square(dims[0]), perimeter_square(dims[0]))
    if shape == "rect":
        return "rect: area=%.4f, perimeter=%.4f" % (area_rect(dims[0], dims[1]),
                                                    perimeter_rect(dims[0], dims[1]))
    if shape == "triangle":
        b, h = dims[0], dims[1]
        peri = b + h + hypotenuse(b, h)
        return "triangle: area=%.4f, perimeter=%.4f" % (area_triangle(b, h), peri)
    raise ValueError("unknown shape: %s" % shape)
