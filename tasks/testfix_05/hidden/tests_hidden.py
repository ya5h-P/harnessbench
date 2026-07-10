from textkit_5 import clamp_577, is_pal_972, c2f_918, dedupe_901, mean2_202

assert clamp_577(5, 1, 10) == 5, 'clamp_577 failed'
assert clamp_577(0, 1, 10) == 1, 'clamp_577 failed'
assert clamp_577(12, 1, 10) == 10, 'clamp_577 failed'
assert clamp_577(-3, -1, 1) == -1, 'clamp_577 failed'
assert is_pal_972('Aba') == True, 'is_pal_972 failed'
assert is_pal_972('No lemon, no melon') == True, 'is_pal_972 failed'
assert is_pal_972('abc') == False, 'is_pal_972 failed'
assert c2f_918(0) == 32.0, 'c2f_918 failed'
assert c2f_918(100) == 212.0, 'c2f_918 failed'
assert c2f_918(-40) == -40.0, 'c2f_918 failed'
assert dedupe_901([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_901 failed'
assert dedupe_901([1, 1, 1]) == [1], 'dedupe_901 failed'
assert dedupe_901([]) == [], 'dedupe_901 failed'
assert mean2_202([2, 4]) == 3.0, 'mean2_202 failed'
assert mean2_202([1, 2, 3]) == 2.0, 'mean2_202 failed'
assert mean2_202([5, 5, 5, 7]) == 5.5, 'mean2_202 failed'

print('hidden tests passed')
