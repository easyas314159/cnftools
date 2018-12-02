"""
"""

__all__ = ['DimacsException', 'dump', 'load']

class DimacsException(Exception):
	"""
	"""
	def __init__(self, msg, lineno, line):
		"""
		"""

		super(DimacsException, self).__init__()

		self.message = msg
		self.lineno = lineno
		self.line = line

def __load_lines(file):
	"""
	"""
	expect_problem = True

	for index, line in enumerate(file):
		line = line.strip()

		if line == '' or line[0] == 'c':
			continue
		elif line[0] == 'p':
			if expect_problem:
				expect_problem = False
			else:
				raise DimacsException('Unexpected problem definition', index, line)
		else:
			if expect_problem:
				raise DimacsException('Syntax error', index, line)

			yield from (int(var) for var in line.split())

def __load_clauses(iterable):
	"""
	"""
	clause = []

	for variable in iterable:
		if variable == 0:
			if clause:
				yield clause
				clause = []
		else:
			clause.append(variable)

	if clause:
		yield clause

def load(file):
	"""
	"""
	yield from __load_clauses(__load_lines(file))

def dump(clauses, file, comment=None):
	"""
	"""

	literals = set()

	# TODO: This is here in case clauses is a generator is there a better way to handl that case?
	clauses = list(clauses)

	for clause in clauses:
		literals.update((abs(l) for l in clause))

	if comment:
		for line in comment.splitlines():
			print('c {comment:s}'.format(comment=line), file=file)

	print('p cnf {literals:d} {clauses:d}'.format(literals=len(literals), clauses=len(clauses)), file=file)

	for clause in clauses:
		print('{clause} 0'.format(clause=' '.join([str(l) for l in clause])), file=file)
