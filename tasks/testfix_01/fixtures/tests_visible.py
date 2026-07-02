from textkit_1 import strip_ext_355, is_pal_650, last_n_666

assert strip_ext_355('archive.tar.gz') == 'archive.tar', 'strip_ext_355 failed'
assert is_pal_650('Aba') == True, 'is_pal_650 failed'
assert last_n_666([1, 2, 3, 4], 2) == [3, 4], 'last_n_666 failed'

print('visible tests passed')
