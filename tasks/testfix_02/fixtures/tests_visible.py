from textkit_2 import between_487, is_pal_367, pct_418, dedupe_560

assert between_487(1, 1, 3) == True, 'between_487 failed'
assert is_pal_367('Aba') == True, 'is_pal_367 failed'
assert pct_418(1, 8) == 12.5, 'pct_418 failed'
assert dedupe_560([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_560 failed'

print('visible tests passed')
