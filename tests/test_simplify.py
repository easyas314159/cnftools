import unittest

import cnftools
from cnftools import simplify

from .fixtures import make_comparable

class CleanTests(unittest.TestCase):
	def test_redundant(self):
		clauses = [[1, 1, 1]]
		cleaned = make_comparable(simplify.clean(clauses))

		self.assertSetEqual(cleaned, make_comparable([[1]]))

	def test_tautology(self):
		clauses = [[1, -1]]
		cleaned = make_comparable(simplify.clean(clauses))

		self.assertSetEqual(cleaned, set())

	def test_combined(self):
		clauses = [[1, 1, 1, 2], [2, 2, -2]]
		cleaned = make_comparable(simplify.clean(clauses))

		self.assertSetEqual(cleaned, make_comparable([[1, 2]]))

class DeduplicateTests(unittest.TestCase):
	def test(self):
		input = [[1, 2], [1, 2]]
		expected = [[1, 2]]

		output = simplify.deduplicate(input)

		self.assertSetEqual(
			make_comparable(output),
			make_comparable(expected)
		)

class UnitPropagateTests(unittest.TestCase):
	def test_single(self):
		clauses = [[-1], [2]]
		cnf_1, cnf_n = simplify.unit_propagate(clauses)

		self.assertSetEqual(cnf_1, set([-1, 2]))
		self.assertListEqual(cnf_n, [])

	def test_cascade(self):
		clauses = [[-1], [-1, 2], [1, 2]]
		cnf_1, cnf_n = simplify.unit_propagate(clauses)

		self.assertSetEqual(cnf_1, set([-1, 2]))
		self.assertListEqual(cnf_n, [])

	def test_contradiction(self):
		clauses = [[-1], [2], [1, -2]]

		cnf_1, cnf_n = simplify.unit_propagate(clauses)

		self.assertSetEqual(cnf_1, set([-1, 2]))
		self.assertSetEqual(make_comparable(cnf_n), make_comparable([[]]))

	def test_trailing(self):
		clauses = [[3, 4]]
		cnf_1, cnf_n = simplify.unit_propagate(clauses)

		self.assertSetEqual(cnf_1, set())
		self.assertSetEqual(make_comparable(cnf_n), make_comparable([[3, 4]]))

class ImpliedUnitsTests(unittest.TestCase):
	def test_single_units(self):
		output = simplify.implied_units([[1]])
		self.assertSetEqual(make_comparable(output), make_comparable([[1]]))

	def test_dual_units(self):
		tests = [
			([[1, 2]], []),
			([[-1, 2]], []),
			([[1, -2]], []),
			([[-1, -2]], []),
			([[-1, -2], [1, -2]], [[-2]]),
			([[-1, 2], [1, 2]], [[2]]),
			([[1, -2], [1, 2]], [[1]]),
			([[-1, -2], [-1, 2]], [[-1]]),
		]

		for input, expected in tests:
			with self.subTest(input):
				output = simplify.implied_units(input)

				self.assertSetEqual(
					make_comparable(output),
					make_comparable(input, expected)
				)

	def test_dual_contradiction(self):
		input = [
			[-1, -2],
			[-1, 2],
			[1, -2],
			[1, 2],
		]

		output = simplify.implied_units(input)
		self.assertSetEqual(
			make_comparable(output),
			make_comparable(input, [[]])
		)

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
		output = simplify.implied_units(input)

		self.assertSetEqual(
			make_comparable(output),
			make_comparable(input, [[]])
		)

	def test_long_units(self):
		input = [[1, 2, 3, 4, 5, 6, 7, 8]]
		output = simplify.implied_units(input)

		self.assertSetEqual(make_comparable(input), make_comparable(output))

class PureLiteralsTests(unittest.TestCase):
	def test_pure_literals(self):
		input = [
			[1, -2, 3, -4],
			[1, 2, -3, -4],
		]
		expected = [
			[1], [-4]
		]

		output = simplify.assign_pure_literals(input)

		self.assertSetEqual(
			make_comparable(output),
			make_comparable(input, expected)
		)

class SubsumedClausesTests(unittest.TestCase):
	def test_subsumption(self):
		input = [
			[1, -2],
			[1, -2, 3],
		]
		expected = [
			[1, -2]
		]

		output = simplify.subsumed_clauses(input)

		self.assertSetEqual(make_comparable(output), make_comparable(expected))
