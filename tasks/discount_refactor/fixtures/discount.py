def final_price(items):
    # items: list of (unit_price, qty). Currently just a naive subtotal.
    total = 0
    for x in items:
        total = total + x[0] * x[1]
    return total
