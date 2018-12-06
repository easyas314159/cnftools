import argparse

import cnftools

def add_arguments(subparser):
	parser = subparser.add_parser(
		'3cnf',
		description='Converts a generalized CNF into 3-CNF using the Tseytin transformation.'
	)
	parser.set_defaults(command=main)

	# TODO: Refactor this to allow reading from stdin
	# TODO: Refactor this to allow writing to stdout
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to the Dimacs CNF file to convert'
	)
	parser.add_argument(
		'-o', '--output',
		type=str,
		required=True,
		help='Path to the resulting 3-CNF equivalent'
	)

	return parser

def main(args):
	with open(args.input, 'r') as file:
		_, _, original = cnftools.load(file)
		transformed = cnftools.to_3cnf(original)

	with open(args.output, 'w') as file:
		cnftools.dump(transformed, file)
