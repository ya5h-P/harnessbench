from textkit_10 import dedupe_934, last_n_440, strip_ext_278, between_256, word_count_486, c2f_187, count_vowels_592, is_pal_687, initials_846

assert dedupe_934([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_934 failed'
assert last_n_440([1, 2, 3, 4], 2) == [3, 4], 'last_n_440 failed'
assert strip_ext_278('archive.tar.gz') == 'archive.tar', 'strip_ext_278 failed'
assert between_256(1, 1, 3) == True, 'between_256 failed'
assert word_count_486('a  b') == 2, 'word_count_486 failed'
assert c2f_187(0) == 32.0, 'c2f_187 failed'
assert count_vowels_592('AeIx') == 3, 'count_vowels_592 failed'
assert is_pal_687('Aba') == True, 'is_pal_687 failed'
assert initials_846('ada lovelace') == 'AL', 'initials_846 failed'

print('visible tests passed')
