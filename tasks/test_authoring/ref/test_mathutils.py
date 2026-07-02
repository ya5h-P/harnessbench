from mathutils import is_prime


def run():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97, 101, 7919]
    composites = [0, 1, 4, 6, 8, 9, 15, 21, 25, 27, 35, 49, 77, 100, 121, 9991]
    for p in primes:
        assert is_prime(p) is True, "is_prime(%d) should be True" % p
    for c in composites:
        assert is_prime(c) is False, "is_prime(%d) should be False" % c
    for n in range(-5, 2):
        assert is_prime(n) is False, "is_prime(%d) should be False" % n
    print("tests passed")


if __name__ == "__main__":
    run()
