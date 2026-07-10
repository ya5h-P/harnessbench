from textkit_8 import mean2_840, strip_ext_426, count_vowels_752, safe_get_868, is_pal_998, clamp_732, running_sum_898

assert mean2_840([2, 4]) == 3.0, 'mean2_840 failed'
assert strip_ext_426('archive.tar.gz') == 'archive.tar', 'strip_ext_426 failed'
assert count_vowels_752('AeIx') == 3, 'count_vowels_752 failed'
assert safe_get_868({'a': 0}, 'a', 9) == 0, 'safe_get_868 failed'
assert is_pal_998('Aba') == True, 'is_pal_998 failed'
assert clamp_732(5, 1, 10) == 5, 'clamp_732 failed'
assert running_sum_898([1, 2, 3]) == [1, 3, 6], 'running_sum_898 failed'

print('visible tests passed')
