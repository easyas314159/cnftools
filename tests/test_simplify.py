import unittest

import cnftools

from .fixtures import make_comparable

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

class ImpliedUnitsTests(unittest.TestCase):
	def test_single_units(self):
		output = cnftools.implied_units([[1]])
		self.assertSetEqual(make_comparable(output), make_comparable([[1]]))

	def test_dual_units(self):
		tests = [
			([[1, 2]], [[1, 2]]),
			([[-1, 2]], [[-1, 2]]),
			([[1, -2]], [[1, -2]]),
			([[-1, -2]], [[-1, -2]]),
			([[-1, -2], [1, -2]], [[-2]]),
			([[-1, 2], [1, 2]], [[2]]),
			([[1, -2], [1, 2]], [[1]]),
			([[-1, -2], [-1, 2]], [[-1]]),
		]

		for input, expected in tests:
			with self.subTest(input):
				output = cnftools.implied_units(input)
				self.assertSetEqual(make_comparable(output), make_comparable(expected))

	def test_dual_contradiction(self):
		input = [
			[-1, -2],
			[-1, 2],
			[1, -2],
			[1, 2],
		]
		output = cnftools.implied_units(input)

		self.assertSetEqual(make_comparable(output), make_comparable([[]]))

	def test_triple_units(self):
		raise unittest.SkipTest()

	def test_triple_contradiction(self):
		input = [
			[-1, -2, -3],
			[-1, 2, -3],
			[1, -2, -3],
			[1, 2, -3],
			[-1, -2, 3],
			[-1, 2, 3],
			[1, -2, 3],
			[1, 2, 3],
		]
		output = cnftools.implied_units(input)

		self.assertSetEqual(make_comparable(output), make_comparable([[]]))

	def test_long_units(self):
		input = [[1, 2, 3, 4, 5, 6, 7, 8]]
		output = cnftools.implied_units(input)

		self.assertSetEqual(make_comparable(input), make_comparable(output))
