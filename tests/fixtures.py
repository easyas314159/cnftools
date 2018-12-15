from itertools import chain

def make_comparable(*clauses):
	return set((frozenset(c) for c in chain(*clauses)))
