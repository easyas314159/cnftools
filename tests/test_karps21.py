import unittest

import networkx as nx

import cnftools

from .fixtures import make_comparable

class ChromaticNumberTests(unittest.TestCase):
	def test_simple(self):
		expected = [
			[1, 2], [3, 4], [5, 6],
			[-1, -2], [-3, -4], [-5, -6],
			[-1, -3], [-2, -4], [-3, -5], [-4, -6]
		]

		graph = nx.Graph()
		nx.add_path(graph, [0, 1, 2])

		output = cnftools.chromatic_number(graph, 2)

		self.assertSetEqual(
			make_comparable(output),
			make_comparable(expected)
		)

	def test_named(self):
		expected = [
			[1, 2], [3, 4], [5, 6],
			[-1, -2], [-3, -4], [-5, -6],
			[-1, -3], [-2, -4], [-3, -5], [-4, -6]
		]

		graph = nx.Graph()
		nx.add_path(graph, ['A', 'B', 'C'])

		output = cnftools.chromatic_number(graph, 2)

		self.assertSetEqual(
			make_comparable(output),
			make_comparable(expected)
		)

class CliqueCoverTests(unittest.TestCase):
	def test_simple(self):
		expected = [
			[1, 2], [3, 4], [5, 6],
			[-1, -2], [-3, -4], [-5, -6],
			[-1, -5], [-2, -6]
		]

		graph = nx.Graph()
		nx.add_path(graph, [0, 1, 2])

		output = cnftools.clique_cover(graph, 2)

		self.assertSetEqual(
			make_comparable(output),
			make_comparable(expected)
		)
