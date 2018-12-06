import argparse
import itertools

from collections import defaultdict

import cnftools

def add_arguments(subparser):
	parser = subparser.add_parser(
		'stats',
		description='Report statistics about a CNF file'
	)
	parser.set_defaults(command=main)

	# TODO: Refactor this to allow reading from stdin
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to the Dimacs CNF file to analyze'
	)

	return parser

def main(args):
	with open(args.input, 'r') as file:
		nliterals, nclauses, clauses = cnftools.load(file)
		clauses = list(clauses)

	literals = set((abs(l) for l in itertools.chain(*clauses)))

	print('Stats for {filename:s}'.format(filename=args.input))

	print('Literals: counted={counted:d} expected={expected:d}'.format(
		counted=len(literals),
		expected=nliterals
	))
	print('Clauses: counted={counted:d} expected={expected:d}'.format(
		counted=len(clauses),
		expected=nclauses
	))

	histogram = defaultdict(list)
	for clause in clauses:
		histogram[len(clause)].append(clause)

	for length in sorted(histogram.keys()):
		print('{nliterals:d}: {nclauses:d}'.format(
			nliterals=length,
			nclauses=len(histogram[length])
		))

		clusters = defaultdict(set)
		for clause in histogram[length]:
			clause = frozenset(clause)
			key = frozenset((abs(l) for l in clause))

			clusters[key].add(clause)

		clustergram = defaultdict(int)
		for cluster in clusters.values():
			clustergram[len(cluster)] += 1

		for length in sorted(clustergram.keys()):
			print('\t{nclauses:d}: {nclusters:d}'.format(
				nclauses=length,
				nclusters=clustergram[length]
			))
