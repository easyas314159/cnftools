import sys

import cnftools

from . import cnfio

def add_arguments(subparser):
	parser = subparser.add_parser(
		'3cnf',
		description='Converts a generalized CNF into 3-CNF using the Tseytin transformation.'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-i', '--input',
		type=str,
		default=None,
		help='Path to the Dimacs CNF file to convert'
	)
	parser.add_argument(
		'-o', '--output',
		type=str,
		default=None,
		help='Path to the resulting 3-CNF equivalent'
	)

	return parser

def main(args):
	with cnfio.open(args.input, sys.stdin, 'r') as file:
		_, _, original = cnftools.load(file)
		transformed = cnftools.to_3cnf(original)

	with cnfio.open(args.output, sys.stdout, 'w') as file:
		cnftools.dump(transformed, file)
