from textkit_4 import c2f_377, initials_945, dedupe_746, count_vowels_392, strip_ext_401

assert c2f_377(0) == 32.0, 'c2f_377 failed'
assert c2f_377(100) == 212.0, 'c2f_377 failed'
assert c2f_377(-40) == -40.0, 'c2f_377 failed'
assert initials_945('ada lovelace') == 'AL', 'initials_945 failed'
assert initials_945('grace') == 'G', 'initials_945 failed'
assert initials_945('alan m turing') == 'AMT', 'initials_945 failed'
assert dedupe_746([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_746 failed'
assert dedupe_746([1, 1, 1]) == [1], 'dedupe_746 failed'
assert dedupe_746([]) == [], 'dedupe_746 failed'
assert count_vowels_392('AeIx') == 3, 'count_vowels_392 failed'
assert count_vowels_392('xyz') == 0, 'count_vowels_392 failed'
assert count_vowels_392('Onomatopoeia') == 8, 'count_vowels_392 failed'
assert strip_ext_401('archive.tar.gz') == 'archive.tar', 'strip_ext_401 failed'
assert strip_ext_401('readme') == 'readme', 'strip_ext_401 failed'
assert strip_ext_401('a.b') == 'a', 'strip_ext_401 failed'

print('hidden tests passed')
