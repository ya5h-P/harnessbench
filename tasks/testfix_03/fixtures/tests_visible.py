from textkit_3 import is_pal_779, safe_get_194, between_413

assert is_pal_779('Aba') == True, 'is_pal_779 failed'
assert safe_get_194({'a': 0}, 'a', 9) == 0, 'safe_get_194 failed'
assert between_413(1, 1, 3) == True, 'between_413 failed'

print('visible tests passed')
