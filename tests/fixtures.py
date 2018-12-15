from itertools import chain

def make_comparable(*clauses):
	return set((frozenset(c) for c in chain(*clauses)))

def count_clauses(*clauses):
	total = 0
	for subclauses in clauses:
		total += len(subclauses)
	return total

def unique_literals(*clauses):
	literals = set()
	for clause in chain(*clauses):
		literals.update((abs(l) for l in clause))
	return literals
