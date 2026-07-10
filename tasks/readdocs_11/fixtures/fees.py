BASE_FEE = None  # TODO: documented under docs/
RATE_PCT = None  # TODO: documented under docs/
MAX_ITEMS = None  # TODO: documented under docs/
GRACE_DAYS = None  # TODO: documented under docs/
SURCHARGE_PCT = None  # TODO: documented under docs/
RETENTION_DAYS = None  # TODO: documented under docs/


def total_fee(amount):
    """round(BASE_FEE + amount * RATE_PCT / 100.0, 2)"""
    raise NotImplementedError
