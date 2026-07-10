from textkit_9 import strip_ext_991, clamp_149, dedupe_170, word_count_537, running_sum_353, safe_get_316, between_844, last_n_638

assert strip_ext_991('archive.tar.gz') == 'archive.tar', 'strip_ext_991 failed'
assert clamp_149(5, 1, 10) == 5, 'clamp_149 failed'
assert dedupe_170([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_170 failed'
assert word_count_537('a  b') == 2, 'word_count_537 failed'
assert running_sum_353([1, 2, 3]) == [1, 3, 6], 'running_sum_353 failed'
assert safe_get_316({'a': 0}, 'a', 9) == 0, 'safe_get_316 failed'
assert between_844(1, 1, 3) == True, 'between_844 failed'
assert last_n_638([1, 2, 3, 4], 2) == [3, 4], 'last_n_638 failed'

print('visible tests passed')
