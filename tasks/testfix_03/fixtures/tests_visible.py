from textkit_3 import is_pal_194, safe_get_413, between_710, strip_ext_874

assert is_pal_194('Aba') == True, 'is_pal_194 failed'
assert safe_get_413({'a': 0}, 'a', 9) == 0, 'safe_get_413 failed'
assert between_710(1, 1, 3) == True, 'between_710 failed'
assert strip_ext_874('archive.tar.gz') == 'archive.tar', 'strip_ext_874 failed'

print('visible tests passed')
