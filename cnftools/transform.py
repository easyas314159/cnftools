"""Utilities for renaming literals
"""

from itertools import chain

def pack(clauses):
	"""Remap the literals in the list of clauses so they map directly to the range 1..N

	Args:

	Returns: :obj:`tuple` - The first element is a :obj:`dict` of :obj:`int` containing
		a mapping of original to remapped literals. The second element is a :obj:`iter`
		of clauses with remapped literals.
	"""

	clauses = list(clauses)

	literals = set((abs(l) for l in chain(*clauses)))

	if 0 in literals:
		raise ValueError('0 is not a valid literal')

	mapping = {}
	for new, old in enumerate(sorted(literals), start=1):
		mapping[old] = new

	return (mapping, remap(clauses, mapping))

def remap(clauses, mapping):
	"""
	"""

	for clause in clauses:
		clause_remapped = []
		for literal in clause:
			if literal > 0:
				clause_remapped.append(mapping[literal])
			elif literal < 0:
				clause_remapped.append(-mapping[-literal])
			else:
				raise ValueError('0 is not a valid literal')

		yield clause_remapped
