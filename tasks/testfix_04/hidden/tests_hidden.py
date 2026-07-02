from textkit_4 import c2f_580, initials_377, dedupe_945, count_vowels_746

assert c2f_580(0) == 32.0, 'c2f_580 failed'
assert c2f_580(100) == 212.0, 'c2f_580 failed'
assert c2f_580(-40) == -40.0, 'c2f_580 failed'
assert initials_377('ada lovelace') == 'AL', 'initials_377 failed'
assert initials_377('grace') == 'G', 'initials_377 failed'
assert initials_377('alan m turing') == 'AMT', 'initials_377 failed'
assert dedupe_945([3, 1, 3, 2]) == [3, 1, 2], 'dedupe_945 failed'
assert dedupe_945([1, 1, 1]) == [1], 'dedupe_945 failed'
assert dedupe_945([]) == [], 'dedupe_945 failed'
assert count_vowels_746('AeIx') == 3, 'count_vowels_746 failed'
assert count_vowels_746('xyz') == 0, 'count_vowels_746 failed'
assert count_vowels_746('Onomatopoeia') == 8, 'count_vowels_746 failed'

print('hidden tests passed')
