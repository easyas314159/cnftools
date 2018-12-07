#!/usr/bin/env python
import argparse

import cnftools

from . import graphs

def add_arguments(subparser):
	parser = subparser.add_parser(
		'chromatic_number',
		description='Generates a CNF expression representing the k-coloring of a graph'
	)
	parser.set_defaults(command=main)

	general = parser.add_argument_group('General settings')
	general.add_argument(
		'-k',
		type=int,
		required=True,
		help='The target chromatic number of the graph'
	)
	# TODO: Add support for writing to stdout
	general.add_argument(
		'-o', '--output',
		type=str,
		required=True,
		help=''
	)

	generators = parser.add_subparsers(
		dest='generator',
		title='Graph generators',
		help='Graph generators'
	)
	# Work around https://bugs.python.org/issue9253
	generators.required = True
	graphs.add_graph_arguments(generators)

	return parser

def main(args):
	clauses = cnftools.karps21.chromatic_number(args.generate(args), args.k)

	comment = '\n'.join([
		'{k:d}-coloring'.format(k=args.k),
		args.describe(args)
	])

	with open(args.output, 'w') as file:
		cnftools.dump(clauses, file, comment=comment)

if __name__ == '__main__':
	main()
