from textkit_12 import safe_get_944, is_pal_873, initials_133, count_vowels_490, last_n_729, pct_274, between_443, dedupe_189, clamp_850, word_count_544, strip_ext_832, running_sum_421

assert safe_get_944({'a': 0}, 'a', 9) == 0, 'safe_get_944 failed'
assert is_pal_873('Aba') == True, 'is_pal_873 failed'
assert initials_133('ada lovelace') == 'AL', 'initials_133 failed'
assert count_vowels_490('AeIx') == 3, 'count_vowels_490 failed'
assert last_n_729([1, 2, 3, 4], 2) == [3, 4], 'last_n_729 failed'
assert pct_274(1, 8) == 12.5, 'pct_274 failed'
assert between_443(1, 1, 3) == True, 'between_443 failed'
assert dedupe_189([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_189 failed'
assert clamp_850(5, 1, 10) == 5, 'clamp_850 failed'
assert word_count_544('a  b') == 2, 'word_count_544 failed'
assert strip_ext_832('archive.tar.gz') == 'archive.tar', 'strip_ext_832 failed'
assert running_sum_421([1, 2, 3]) == [1, 3, 6], 'running_sum_421 failed'

print('visible tests passed')
