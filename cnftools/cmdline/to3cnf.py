import argparse

import cnftools

def get_cli_arguments():
	parser = argparse.ArgumentParser(
		description='Converts a generalized CNF into 3-CNF using the Tseytin transformation.'
	)

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

	return parser.parse_args()

def main():
	args = get_cli_arguments()

	with open(args.input, 'r') as file:
		original = list(cnftools.load(file))

	transformed = cnftools.to_3cnf(original)

	with open(args.output, 'w') as file:
		cnftools.dump(transformed, file)

if __name__ == '__main__':
	main()
