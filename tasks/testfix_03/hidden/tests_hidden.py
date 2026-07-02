from textkit_3 import is_pal_779, safe_get_194, between_413

assert is_pal_779('Aba') == True, 'is_pal_779 failed'
assert is_pal_779('No lemon, no melon') == True, 'is_pal_779 failed'
assert is_pal_779('abc') == False, 'is_pal_779 failed'
assert safe_get_194({'a': 0}, 'a', 9) == 0, 'safe_get_194 failed'
assert safe_get_194({'a': 5}, 'b', 7) == 7, 'safe_get_194 failed'
assert safe_get_194({}, 'x', None) == None, 'safe_get_194 failed'
assert between_413(1, 1, 3) == True, 'between_413 failed'
assert between_413(3, 1, 3) == True, 'between_413 failed'
assert between_413(2, 1, 3) == True, 'between_413 failed'
assert between_413(4, 1, 3) == False, 'between_413 failed'

print('hidden tests passed')
