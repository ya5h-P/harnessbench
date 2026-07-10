from textkit_11 import is_pal_560, last_n_700, dedupe_343, count_vowels_800, safe_get_478, c2f_550, clamp_559, mean2_631, running_sum_187, pct_336

assert is_pal_560('Aba') == True, 'is_pal_560 failed'
assert last_n_700([1, 2, 3, 4], 2) == [3, 4], 'last_n_700 failed'
assert dedupe_343([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_343 failed'
assert count_vowels_800('AeIx') == 3, 'count_vowels_800 failed'
assert safe_get_478({'a': 0}, 'a', 9) == 0, 'safe_get_478 failed'
assert c2f_550(0) == 32.0, 'c2f_550 failed'
assert clamp_559(5, 1, 10) == 5, 'clamp_559 failed'
assert mean2_631([2, 4]) == 3.0, 'mean2_631 failed'
assert running_sum_187([1, 2, 3]) == [1, 3, 6], 'running_sum_187 failed'
assert pct_336(1, 8) == 12.5, 'pct_336 failed'

print('visible tests passed')
