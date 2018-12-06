import argparse

from . import chromaticnumber
from . import cliquecover

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
		description='Available sub-commands'
	)
	# Work around https://bugs.python.org/issue9253
	karpsparser.required = True

	chromaticnumber.add_arguments(karpsparser)
	cliquecover.add_arguments(karpsparser)

	return parser

__all__ = ['add_arguments']
