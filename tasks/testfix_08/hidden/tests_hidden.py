from textkit_8 import mean2_145, strip_ext_318, count_vowels_840, safe_get_426, is_pal_752

assert mean2_145([2, 4]) == 3.0, 'mean2_145 failed'
assert mean2_145([1, 2, 3]) == 2.0, 'mean2_145 failed'
assert mean2_145([5, 5, 5, 7]) == 5.5, 'mean2_145 failed'
assert strip_ext_318('archive.tar.gz') == 'archive.tar', 'strip_ext_318 failed'
assert strip_ext_318('readme') == 'readme', 'strip_ext_318 failed'
assert strip_ext_318('a.b') == 'a', 'strip_ext_318 failed'
assert count_vowels_840('AeIx') == 3, 'count_vowels_840 failed'
assert count_vowels_840('xyz') == 0, 'count_vowels_840 failed'
assert count_vowels_840('Onomatopoeia') == 8, 'count_vowels_840 failed'
assert safe_get_426({'a': 0}, 'a', 9) == 0, 'safe_get_426 failed'
assert safe_get_426({'a': 5}, 'b', 7) == 7, 'safe_get_426 failed'
assert safe_get_426({}, 'x', None) == None, 'safe_get_426 failed'
assert is_pal_752('Aba') == True, 'is_pal_752 failed'
assert is_pal_752('No lemon, no melon') == True, 'is_pal_752 failed'
assert is_pal_752('abc') == False, 'is_pal_752 failed'

print('hidden tests passed')
