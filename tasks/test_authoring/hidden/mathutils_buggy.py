def is_prime(n):
    # BUG: only checks divisibility by 2 and 3, so 25, 49, 77, ... are wrongly "prime"
    if n < 2:
        return False
    for d in (2, 3):
        if n % d == 0 and n != d:
            return False
    return True
