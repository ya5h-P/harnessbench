def final_price(items):
    subtotal = 0.0
    for unit_price, qty in items:
        line = unit_price * qty
        if qty >= 10:
            line *= 0.95
        subtotal += line
    if subtotal >= 500:
        subtotal *= 0.92
    return round(subtotal, 2)
