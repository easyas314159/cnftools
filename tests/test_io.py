import unittest
import functools

from io import StringIO

from cnftools import io

from .fixtures import *

class LoadTests(unittest.TestCase):
	def test_invalid_problem(self):
		tests = [
			'', # Empty file
			'This is a a line', # No problem statement
			# Invalid problem statements
			'p not_cnf 1 1',
			'p cnf 1 2 3',
			'p cnf 1',
			# Invalid counts
			'p cnf -1 1',
			'p cnf 1 -1',
			'p cnf bacon 1',
			'p cnf 1 waffles',
		]

		for input in tests:
			with self.subTest(input):
				cnf = StringIO(input)
				self.assertRaises(io.DimacsException, functools.partial(io.load, cnf))

	def test_invalid_clause(self):
		tests = [
			# Invalid literal
			'''
			p cnf 1 1
			bacon 0
			''',
		]

		for input in tests:
			with self.subTest(input):
				cnf = StringIO(input)

				nliterals, nclauses, clauses = io.load(cnf)

				self.assertRaises(io.DimacsException, functools.partial(list, clauses))

	def test_success(self):
		tests = [
			(
				'''
				c This is a comment
				p cnf 0 0
				''',
				[]
			),
			(
				'''

				p cnf 0 0
				''',
				[]
			),
			(
				'''
				c Correct
				p cnf 2 1
				1 2 0
				''',
				[[1, 2]]
			),
			(
				'''
				c No trailing 0
				p cnf 2 1
				1 2
				''',
				[[1, 2]]
			),
			(
				'''
				c Contradiction
				p cnf 0 1
				0
				''',
				[[]]
			)
		]

		for input, expected in tests:
			with self.subTest(input):
				cnf = StringIO(input)

				expected_nliterals = len(unique_literals(expected))
				expected_nclauses = count_clauses(expected)

				nliterals, nclauses, clauses = io.load(cnf)

				self.assertEqual(nliterals, expected_nliterals)
				self.assertEqual(nclauses, expected_nclauses)

				self.assertSetEqual(
					make_comparable(clauses),
					make_comparable(expected)
				)
