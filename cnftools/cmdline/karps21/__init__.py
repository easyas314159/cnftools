import argparse

from . import coloring

def add_arguments(subparser):
	parser = subparser.add_parser(
		'karps21',
		description='Converts a generalized CNF into 3-CNF using the Tseytin transformation.'
	)

	karpsparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		required=True
	)

	coloring.add_arguments(karpsparser)

	return parser

__all__ = ['add_arguments']
