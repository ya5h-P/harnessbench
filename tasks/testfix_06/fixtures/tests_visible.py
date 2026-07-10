from textkit_6 import safe_get_276, strip_ext_225, clamp_246, dedupe_717, pct_561, count_vowels_486

assert safe_get_276({'a': 0}, 'a', 9) == 0, 'safe_get_276 failed'
assert strip_ext_225('archive.tar.gz') == 'archive.tar', 'strip_ext_225 failed'
assert clamp_246(5, 1, 10) == 5, 'clamp_246 failed'
assert dedupe_717([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_717 failed'
assert pct_561(1, 8) == 12.5, 'pct_561 failed'
assert count_vowels_486('AeIx') == 3, 'count_vowels_486 failed'

print('visible tests passed')
