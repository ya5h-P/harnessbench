from textkit_6 import safe_get_310, strip_ext_237, clamp_276, dedupe_225

assert safe_get_310({'a': 0}, 'a', 9) == 0, 'safe_get_310 failed'
assert strip_ext_237('archive.tar.gz') == 'archive.tar', 'strip_ext_237 failed'
assert clamp_276(5, 1, 10) == 5, 'clamp_276 failed'
assert dedupe_225([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_225 failed'

print('visible tests passed')
