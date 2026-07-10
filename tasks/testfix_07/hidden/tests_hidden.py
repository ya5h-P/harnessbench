from textkit_7 import between_409, dedupe_869, pct_208, clamp_892, initials_499, safe_get_219

assert between_409(1, 1, 3) == True, 'between_409 failed'
assert between_409(3, 1, 3) == True, 'between_409 failed'
assert between_409(2, 1, 3) == True, 'between_409 failed'
assert between_409(4, 1, 3) == False, 'between_409 failed'
assert dedupe_869([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_869 failed'
assert dedupe_869([1, 1, 1]) == [1], 'dedupe_869 failed'
assert dedupe_869([]) == [], 'dedupe_869 failed'
assert pct_208(1, 8) == 12.5, 'pct_208 failed'
assert pct_208(1, 4) == 25.0, 'pct_208 failed'
assert pct_208(3, 3) == 100.0, 'pct_208 failed'
assert clamp_892(5, 1, 10) == 5, 'clamp_892 failed'
assert clamp_892(0, 1, 10) == 1, 'clamp_892 failed'
assert clamp_892(12, 1, 10) == 10, 'clamp_892 failed'
assert clamp_892(-3, -1, 1) == -1, 'clamp_892 failed'
assert initials_499('ada lovelace') == 'AL', 'initials_499 failed'
assert initials_499('grace') == 'G', 'initials_499 failed'
assert initials_499('alan m turing') == 'AMT', 'initials_499 failed'
assert safe_get_219({'a': 0}, 'a', 9) == 0, 'safe_get_219 failed'
assert safe_get_219({'a': 5}, 'b', 7) == 7, 'safe_get_219 failed'
assert safe_get_219({}, 'x', None) == None, 'safe_get_219 failed'

print('hidden tests passed')
