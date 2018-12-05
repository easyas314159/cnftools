def clean(clauses):
	for clause in clauses:
		# Simplify (L | ... | L) to (L)
		clause = set(clause)

		# If clause contains (L | -L) then it is always true so we can skip it
		if len(clause) != len(set((abs(l) for l in clause))):
			continue

		yield clause

def unit_propagate(clauses, cascade=True):
	cnf_1, cnf_n = set(), set()
	cnf_other = list()

	for clause in clauses:
		if len(clause) == 1:
			cnf_1.add(list(clause)[0])
		else:
			cnf_other.append(clause)

	if not cnf_1:
		return cnf_1, cnf_other

	for clause in cnf_other:
		clause = set(clause)
		for l in list(clause):
			# Remove clauses containing True literals
			if l in cnf_1:
				break
			# Remove false literals from clauses
			if -l in cnf_1:
				clause.remove(l)
		else:
			cnf_n.add(frozenset(clause))

	if cascade:
		cnf_1_next, cnf_n = unit_propagate(cnf_n)
		cnf_1.update(cnf_1_next)

	return cnf_1, cnf_n

def simplify(clauses):
	# Remove duplicate clauses
	cnf_n = set((frozenset(c) for c in clean(clauses)))
	cnf_1 = set()

	modified = True
	while modified:
		modified = False

		cnf_1_new, cnf_n = unit_propagate(cnf_n)
		cnf_1.update(cnf_1_new)

		if cnf_1_new:
			modified = True

		# TODO: Solve for implied literals
		# TODO: Remove subsumed clauses (e.g. (a|b) => (a|b|c))

	yield from (set([l]) for l in cnf_1)
	yield from cnf_n
