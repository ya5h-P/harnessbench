import sys


def greet(name):
    return "Hello, " + name + "!"


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(greet(a))
