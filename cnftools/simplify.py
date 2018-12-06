from collections import defaultdict

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

IMPLICATIONS = {
	2: {12: [None, True], 10: [True, None], 14: [True, True], 5: [False, None], 13: [False, True], 3: [None, False], 11: [True, False], 7: [False, False], 15: None},
	3: {240: [None, None, True], 248: [None, None, True], 244: [None, None, True], 204: [None, True, None], 236: [None, True, None], 220: [None, True, None], 252: [None, True, True], 242: [None, None, True], 170: [True, None, None], 234: [True, None, None], 186: [True, None, None], 250: [True, None, True], 246: [None, None, True], 206: [None, True, None], 174: [True, None, None], 238: [True, True, None], 222: [None, True, None], 190: [True, None, None], 254: [True, True, True], 241: [None, None, True], 249: [None, None, True], 85: [False, None, None], 213: [False, None, None], 117: [False, None, None], 245: [False, None, True], 205: [None, True, None], 237: [None, True, None], 93: [False, None, None], 221: [False, True, None], 125: [False, None, None], 253: [False, True, True], 51: [None, False, None], 179: [None, False, None], 115: [None, False, None], 243: [None, False, True], 171: [True, None, None], 235: [True, None, None], 59: [None, False, None], 187: [True, False, None], 123: [None, False, None], 251: [True, False, True], 87: [False, None, None], 215: [False, None, None], 55: [None, False, None], 183: [None, False, None], 119: [False, False, None], 247: [False, False, True], 15: [None, None, False], 143: [None, None, False], 79: [None, None, False], 207: [None, True, False], 47: [None, None, False], 175: [True, None, False], 111: [None, None, False], 239: [True, True, False], 31: [None, None, False], 159: [None, None, False], 95: [False, None, False], 223: [False, True, False], 63: [None, False, False], 191: [True, False, False], 127: [False, False, False], 255: None},
}

def implied_units(clauses):
	clusters = defaultdict(list)
	for clause in clauses:
		if len(clause) == 1:
			yield clause
			continue

		key = frozenset((abs(l) for l in clause))
		if len(key) != len(clause):
			yield clause
			# {KL}: Should this maybe throw an exception here?
			continue

		if not len(key) in IMPLICATIONS:
			yield clause
			continue

		key = tuple(sorted(key))
		clusters[key].append(list(sorted(clause, key=abs)))

	# TODO: There is significant room for improved record keeping here
	temp = defaultdict(int)
	for key, cluster in clusters.items():
		code_cluster = 0
		for clause in cluster:
			code_clause = 0
			for index, literal in enumerate(clause):
				if literal > 0:
					code_clause |= 1 << index
			code_cluster |= 1 << code_clause

		implications = IMPLICATIONS[len(key)]
		if not code_cluster in implications:
			yield from cluster
		else:
			if implications[code_cluster] is None:
				yield []
			else:
				for literal, value in zip(key, implications[code_cluster]):
					if value is None:
						continue
					cluster.append([literal if value else -literal])
				cnf_1, cnf_n = unit_propagate(cluster)

				yield from (list([l]) for l in cnf_1)
				yield from cnf_n

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
