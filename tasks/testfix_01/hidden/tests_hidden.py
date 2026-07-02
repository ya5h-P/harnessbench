from textkit_1 import strip_ext_355, is_pal_650, last_n_666

assert strip_ext_355('archive.tar.gz') == 'archive.tar', 'strip_ext_355 failed'
assert strip_ext_355('readme') == 'readme', 'strip_ext_355 failed'
assert strip_ext_355('a.b') == 'a', 'strip_ext_355 failed'
assert is_pal_650('Aba') == True, 'is_pal_650 failed'
assert is_pal_650('No lemon, no melon') == True, 'is_pal_650 failed'
assert is_pal_650('abc') == False, 'is_pal_650 failed'
assert last_n_666([1, 2, 3, 4], 2) == [3, 4], 'last_n_666 failed'
assert last_n_666([1, 2], 5) == [1, 2], 'last_n_666 failed'
assert last_n_666([7], 1) == [7], 'last_n_666 failed'

print('hidden tests passed')
