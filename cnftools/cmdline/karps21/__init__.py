import argparse

from . import coloring
from . import clique

def add_arguments(subparser):
	parser = subparser.add_parser(
		'karps21',
		description="""
		Tools for generating CNF files representing Karp\'s 21 NP-Complete problems.

		See: Karp, Richard M. "Reducibility among combinatorial problems." Complexity of computer computations. Springer, Boston, MA, 1972. 85-103.
		"""
	)

	karpsparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		required=True
	)

	coloring.add_arguments(karpsparser)
	clique.add_arguments(karpsparser)

	return parser

__all__ = ['add_arguments']
