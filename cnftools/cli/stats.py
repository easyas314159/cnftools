import sys
import itertools

from collections import defaultdict

import cnftools

from . import cnfio

def add_arguments(subparser):
	parser = subparser.add_parser(
		'stats',
		description='Report statistics about a CNF file'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-i', '--input',
		type=str,
		default=None,
		help='Path to the Dimacs CNF file to analyze'
	)

	return parser

def main(args):
	with cnfio.open(args.input, sys.stdin, 'r') as file:
		nliterals, nclauses, clauses = cnftools.load(file)
		clauses = list(clauses)

	literals = set((abs(l) for l in itertools.chain(*clauses)))

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

		for nclauses in sorted(clustergram.keys()):
			print('\t{nclauses:d}: {nclusters:d}'.format(
				nclauses=nclauses,
				nclusters=clustergram[nclauses]
			))
