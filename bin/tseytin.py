#!/usr/bin/env python
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

def tseytin_transform(clauses):
	literals = set()
	for clause in clauses:
		literals.update((abs(l) for l in clause))

	max_literal = max(literals)

	for clause in clauses:
		while len(clause) > 3:
			next_clause = list()
			for i in range(0, len(clause), 2):
				if i+1 < len(clause):
					max_literal += 1
					next_clause.append(max_literal)
					yield [clause[i], clause[i+1], -max_literal]
				else:
					next_clause.append(clause[i])
			clause = next_clause

		yield clause

def main():
	args = get_cli_arguments()

	with open(args.input, 'r') as file:
		original = list(cnftools.load(file))

	transformed = tseytin_transform(original)

	with open(args.output, 'w') as file:
		cnftools.dump(transformed, file)

if __name__ == '__main__':
	main()
