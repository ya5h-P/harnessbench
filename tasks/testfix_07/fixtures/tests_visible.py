from textkit_7 import between_293, dedupe_409, pct_869, clamp_208, initials_892

assert between_293(1, 1, 3) == True, 'between_293 failed'
assert dedupe_409([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_409 failed'
assert pct_869(1, 8) == 12.5, 'pct_869 failed'
assert clamp_208(5, 1, 10) == 5, 'clamp_208 failed'
assert initials_892('ada lovelace') == 'AL', 'initials_892 failed'

print('visible tests passed')
