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
