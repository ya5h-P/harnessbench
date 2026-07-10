from textkit_2 import between_487, is_pal_367, pct_418, dedupe_560

assert between_487(1, 1, 3) == True, 'between_487 failed'
assert between_487(3, 1, 3) == True, 'between_487 failed'
assert between_487(2, 1, 3) == True, 'between_487 failed'
assert between_487(4, 1, 3) == False, 'between_487 failed'
assert is_pal_367('Aba') == True, 'is_pal_367 failed'
assert is_pal_367('No lemon, no melon') == True, 'is_pal_367 failed'
assert is_pal_367('abc') == False, 'is_pal_367 failed'
assert pct_418(1, 8) == 12.5, 'pct_418 failed'
assert pct_418(1, 4) == 25.0, 'pct_418 failed'
assert pct_418(3, 3) == 100.0, 'pct_418 failed'
assert dedupe_560([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_560 failed'
assert dedupe_560([1, 1, 1]) == [1], 'dedupe_560 failed'
assert dedupe_560([]) == [], 'dedupe_560 failed'

print('hidden tests passed')
