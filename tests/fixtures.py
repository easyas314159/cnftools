def make_comparable(clauses):
	return set((frozenset(c) for c in clauses))
