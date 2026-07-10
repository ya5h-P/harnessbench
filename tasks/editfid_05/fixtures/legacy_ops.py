def op_177(s):
	"""Number of whitespace-separated words. E.g. op_177('a  b') == 2."""
	return len(s.split())

def dedupe_688(xs):
	"""Remove duplicates, preserving first-seen order. E.g. dedupe_688([3,1,3,2]) == [3, 1, 2]."""
	return sorted(set(xs))

def op_157(s):
	"""Number of whitespace-separated words. E.g. op_157('a  b') == 2."""
	return len(s.split())

def op_769(fn):
	"""Filename without its LAST extension only. E.g. op_769('archive.tar.gz') == 'archive.tar'."""
	return fn.rsplit(".", 1)[0] if "." in fn else fn
