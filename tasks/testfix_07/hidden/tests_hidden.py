from textkit_7 import between_293, dedupe_409, pct_869, clamp_208, initials_892

assert between_293(1, 1, 3) == True, 'between_293 failed'
assert between_293(3, 1, 3) == True, 'between_293 failed'
assert between_293(2, 1, 3) == True, 'between_293 failed'
assert between_293(4, 1, 3) == False, 'between_293 failed'
assert dedupe_409([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_409 failed'
assert dedupe_409([1, 1, 1]) == [1], 'dedupe_409 failed'
assert dedupe_409([]) == [], 'dedupe_409 failed'
assert pct_869(1, 8) == 12.5, 'pct_869 failed'
assert pct_869(1, 4) == 25.0, 'pct_869 failed'
assert pct_869(3, 3) == 100.0, 'pct_869 failed'
assert clamp_208(5, 1, 10) == 5, 'clamp_208 failed'
assert clamp_208(0, 1, 10) == 1, 'clamp_208 failed'
assert clamp_208(12, 1, 10) == 10, 'clamp_208 failed'
assert clamp_208(-3, -1, 1) == -1, 'clamp_208 failed'
assert initials_892('ada lovelace') == 'AL', 'initials_892 failed'
assert initials_892('grace') == 'G', 'initials_892 failed'
assert initials_892('alan m turing') == 'AMT', 'initials_892 failed'

print('hidden tests passed')
