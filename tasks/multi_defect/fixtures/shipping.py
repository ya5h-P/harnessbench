def quote(weight_kg, distance_km, express=False):
    # BUGGY: wrong distance rate, no surcharge, ignores express, no minimum
    base = 5.0
    cost = base + 0.5 * weight_kg + 0.05 * distance_km
    return round(cost, 2)
