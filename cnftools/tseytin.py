#!/usr/bin/env python
__all__ = ['to_3cnf']

def to_3cnf(clauses):
	clauses = list(clauses)

	literals = set()
	for clause in clauses:
		literals.update((abs(l) for l in clause))

	max_literal = max(literals)

	for clause in clauses:
		clause = list(sorted(clause, key=abs))
		while len(clause) > 3:
			next_clause = list()
			for i in range(0, len(clause), 2):
				if i+1 < len(clause):
					max_literal += 1
					next_clause.append(max_literal)
					yield [clause[i], clause[i+1], -max_literal]
				else:
					next_clause.append(clause[i])
			clause = next_clause

		yield clause
