def simplify(clauses):
	cnf_1, cnf_n = set(), set()
	for original in clauses:
		# Make sure to simplify (L | ... | L) to (L)
		clause = frozenset(original)

		# If clause contains (L | -L) then it is always true so we can skip it
		if len(clause) != len(set((abs(l) for l in clause))):
			continue

		# Remove duplicate clauses
		if (len(clause) == 1):
			cnf_1.add(list(clause)[0])
		else:
			cnf_n.add(clause)

	modified = True
	while modified:
		cnf_next = set()
		modified = False
		for clause in cnf_n:
			clause = set(clause)
			for l in list(clause):
				# Remove clauses containing True literals
				if l in cnf_1:
					modified = True
					break

				# Remove false literals from clauses
				if -l in cnf_1:
					modified = True
					clause.remove(l)
			else:
				cnf_next.add(frozenset(clause))

		# TODO: Solve for implied literals
		# TODO: Remove subsumed clauses (e.g. (a|b) => (a|b|c))

		cnf_n = set()
		for clause in cnf_next:
			if (len(clause) == 1):
				cnf_1.add(list(clause)[0])
			else:
				cnf_n.add(clause)

	yield from (set([l]) for l in cnf_1)
	yield from cnf_n
