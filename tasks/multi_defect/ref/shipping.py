def quote(weight_kg, distance_km, express=False):
    cost = 5.0 + 0.5 * weight_kg + 0.1 * distance_km
    if weight_kg > 30:
        cost += 20.0
    if express:
        cost *= 1.5
    if cost < 10.0:
        cost = 10.0
    return round(cost, 2)
