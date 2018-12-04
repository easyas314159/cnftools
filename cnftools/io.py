"""Functions to loading and saving Dimacs CNF files.
"""
import re

__all__ = ['DimacsException', 'dump', 'load']

class DimacsException(Exception):
	"""
	"""
	def __init__(self, message, lineno, line):
		"""
		"""

		super(DimacsException, self).__init__('{message:s}[{lineno:d}]: {line:s}'.format(
			message=message, lineno=lineno, line=line
		))

		self.lineno = lineno
		self.line = line

def __load_lines(file):
	"""Load lines from a Dimacs CNF file while striping out comments and empty lines"""
	for lineno, line in enumerate(file, start=1):
		line = line.strip()
		if line == '' or line[0] == 'c':
			continue
		yield (lineno, line)

LITERAL_TEST = re.compile('-?[1-9][0-9]*')

def __load_literals(iterable):
	"""Create a stream of literals from lines
	"""
	for lineno, line in iterable:
		for literal in line.split():
			if not (literal == '0' or LITERAL_TEST.match(literal)):
				raise DimacsException('Syntax error', lineno, line)
			yield int(literal)

def __load_clauses(iterable):
	"""Given an iterable of literals construct clauses spliting on 0
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
	"""Load a Dimacs CNF file
	"""

	lines = __load_lines(file)

	# The first line we get should be a problem definition
	lineno, line = next(lines)
	if line[0] != 'p':
		raise DimacsException('Expected problem definition', lineno, line)

	# Validate the problem definition
	problem = line.split()
	if not (len(problem) == 4 and problem[0] == 'p' and problem[1] == 'cnf'):
		raise DimacsException('Invalid problem definition', lineno, line)

	try:
		nliterals = int(problem[2])
		if nliterals < 0:
			raise DimacsException('Negative literal count', lineno, line)
	except ValueError:
		raise DimacsException('Invalid literal count', lineno, line)

	try:
		nclauses = int(problem[3])
		if nclauses < 0:
			raise DimacsException('Negative clause count', lineno, line)
	except ValueError:
		raise DimacsException('Invalid clause count', lineno, line)

	# Create stream of literals
	literals = __load_literals(lines)
	# Convert literal stream into clauses
	clauses = __load_clauses(literals)
	# Return the header and a clause generator
	return (
		nliterals,
		nclauses,
		clauses
	)

def dump(clauses, file, comment=None):
	"""Write a collection of clauses to to file in Dimacs CNF format
	"""

	literals = set()
	clauses = list(clauses)

	for clause in clauses:
		literals.update((abs(l) for l in clause))

	if comment:
		for line in comment.splitlines():
			print('c {comment:s}'.format(comment=line), file=file)

	print('p cnf {literals:d} {clauses:d}'.format(literals=len(literals), clauses=len(clauses)), file=file)

	for clause in clauses:
		print('{clause} 0'.format(clause=' '.join([str(l) for l in clause])), file=file)
