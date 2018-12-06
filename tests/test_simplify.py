import unittest

import cnftools

def make_comparable(clauses):
	return set((frozenset(c) for c in clauses))

class CleanTests(unittest.TestCase):
	def test_redundant(self):
		clauses = [[1, 1, 1]]
		cleaned = make_comparable(cnftools.clean(clauses))

		self.assertSetEqual(cleaned, make_comparable([[1]]))

	def test_tautology(self):
		clauses = [[1, -1]]
		cleaned = make_comparable(cnftools.clean(clauses))

		self.assertSetEqual(cleaned, set())

	def test_combined(self):
		clauses = [[1, 1, 1, 2], [2, 2, -2]]
		cleaned = make_comparable(cnftools.clean(clauses))

		self.assertSetEqual(cleaned, make_comparable([[1, 2]]))

class UnitPropagateTests(unittest.TestCase):
	def test_single(self):
		clauses = [[-1], [2]]
		cnf_1, cnf_n = cnftools.unit_propagate(clauses)

		self.assertSetEqual(cnf_1, set([-1, 2]))
		self.assertListEqual(cnf_n, [])

	def test_cascade(self):
		clauses = [[-1], [-1, 2], [1, 2]]
		cnf_1, cnf_n = cnftools.unit_propagate(clauses)

		self.assertSetEqual(cnf_1, set([-1, 2]))
		self.assertListEqual(cnf_n, [])

	def test_contradiction(self):
		clauses = [[-1], [2], [1, -2]]

		cnf_1, cnf_n = cnftools.unit_propagate(clauses)

		self.assertSetEqual(cnf_1, set([-1, 2]))
		self.assertSetEqual(make_comparable(cnf_n), make_comparable([[]]))

	def test_trailing(self):
		clauses = [[3, 4]]
		cnf_1, cnf_n = cnftools.unit_propagate(clauses)

		self.assertSetEqual(cnf_1, set())
		self.assertSetEqual(make_comparable(cnf_n), make_comparable([[3, 4]]))
