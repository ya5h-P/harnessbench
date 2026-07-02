from textkit_8 import mean2_145, strip_ext_318, count_vowels_840, safe_get_426, is_pal_752

assert mean2_145([2, 4]) == 3.0, 'mean2_145 failed'
assert strip_ext_318('archive.tar.gz') == 'archive.tar', 'strip_ext_318 failed'
assert count_vowels_840('AeIx') == 3, 'count_vowels_840 failed'
assert safe_get_426({'a': 0}, 'a', 9) == 0, 'safe_get_426 failed'
assert is_pal_752('Aba') == True, 'is_pal_752 failed'

print('visible tests passed')
