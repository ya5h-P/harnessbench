from textkit_3 import is_pal_194, safe_get_413, between_710, strip_ext_874

assert is_pal_194('Aba') == True, 'is_pal_194 failed'
assert is_pal_194('No lemon, no melon') == True, 'is_pal_194 failed'
assert is_pal_194('abc') == False, 'is_pal_194 failed'
assert safe_get_413({'a': 0}, 'a', 9) == 0, 'safe_get_413 failed'
assert safe_get_413({'a': 5}, 'b', 7) == 7, 'safe_get_413 failed'
assert safe_get_413({}, 'x', None) == None, 'safe_get_413 failed'
assert between_710(1, 1, 3) == True, 'between_710 failed'
assert between_710(3, 1, 3) == True, 'between_710 failed'
assert between_710(2, 1, 3) == True, 'between_710 failed'
assert between_710(4, 1, 3) == False, 'between_710 failed'
assert strip_ext_874('archive.tar.gz') == 'archive.tar', 'strip_ext_874 failed'
assert strip_ext_874('readme') == 'readme', 'strip_ext_874 failed'
assert strip_ext_874('a.b') == 'a', 'strip_ext_874 failed'

print('hidden tests passed')
