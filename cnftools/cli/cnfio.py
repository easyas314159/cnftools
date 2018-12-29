from contextlib import contextmanager

@contextmanager
def open(file, fallback, *args, **kwargs):
	if file is None:
		# TODO: How should this handle broken pipe errors?
		yield fallback
	else:
		with open(file, *args, **kwargs) as f:
			yield f
