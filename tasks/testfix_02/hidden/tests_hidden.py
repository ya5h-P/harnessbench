from textkit_2 import between_434, is_pal_487, pct_367

assert between_434(1, 1, 3) == True, 'between_434 failed'
assert between_434(3, 1, 3) == True, 'between_434 failed'
assert between_434(2, 1, 3) == True, 'between_434 failed'
assert between_434(4, 1, 3) == False, 'between_434 failed'
assert is_pal_487('Aba') == True, 'is_pal_487 failed'
assert is_pal_487('No lemon, no melon') == True, 'is_pal_487 failed'
assert is_pal_487('abc') == False, 'is_pal_487 failed'
assert pct_367(1, 8) == 12.5, 'pct_367 failed'
assert pct_367(1, 4) == 25.0, 'pct_367 failed'
assert pct_367(3, 3) == 100.0, 'pct_367 failed'

print('hidden tests passed')
