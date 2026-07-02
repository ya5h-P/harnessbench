def op_682(c):
	"""Celsius to Fahrenheit. E.g. op_682(0) == 32.0; op_682(100) == 212.0."""
	return c * 9 / 5 + 32

def dedupe_688(xs):
	"""Remove duplicates, preserving first-seen order. E.g. dedupe_688([3,1,3,2]) == [3, 1, 2]."""
	return sorted(set(xs))

def op_218(x, lo, hi):
	"""True iff lo <= x <= hi (inclusive). E.g. op_218(1, 1, 3) is True."""
	return lo <= x <= hi

def op_473(c):
	"""Celsius to Fahrenheit. E.g. op_473(0) == 32.0; op_473(100) == 212.0."""
	return c * 9 / 5 + 32
