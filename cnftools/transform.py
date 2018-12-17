"""Utilities for renaming literals
"""

from itertools import chain

def pack(clauses):
	"""Remap the literals in the list of clauses so they map directly to the
	range 1..N. The literals will be remapped to the range 1..N in ascending
	numerical order.

	Args:
		clauses (:obj:`iter` of :obj:`iter` of :obj:`int`): A collection of clauses
			to remap

	Raises:
		ValueError: If 0 is a literal in the supplied clauses

	Returns: :obj:`dict` of :obj:`int` containing a mapping of original to remapped literals.
	"""

	clauses = list(clauses)

	literals = set((abs(l) for l in chain(*clauses)))

	if 0 in literals:
		raise ValueError('0 is not a valid literal')

	return {old:new for new, old in enumerate(sorted(literals), start=1)}

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
