import random

import cnftools

def add_arguments(subparser):
	parser = subparser.add_parser(
		'shuffle',
		description='Randomly shuffle clauses and literals in a Dimacs CNF file. The resulting CNF file will be equisatisfiable.'
	)
	parser.set_defaults(command=main)

	# TODO: Refactor this to allow reading from stdin
	# TODO: Refactor this to allow writing to stdout
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to the Dimacs CNF file to shuffle'
	)
	parser.add_argument(
		'-o', '--output',
		type=str,
		required=True,
		help='Path to the resulting shuffled CNF'
	)

	parser.add_argument(
		'-s', '--seed',
		type=int,
		default=None,
		help='Set the seed value for the random number generator. If not set the current system time is used.'
	)

	parser.add_argument(
		'-c', '--clauses',
		default=False,
		action='store_true',
		help='Shuffle the order of clauses.'
	)

	parser.add_argument(
		'-l', '--literals',
		default=False,
		action='store_true',
		help='Shuffle the order of literals within clauses.'
	)

	parser.add_argument(
		'-v', '--variables',
		default=False,
		action='store_true',
		help='Randomly rename variables.'
	)

	return parser

def main(args):
	if not args.seed is None:
		random.seed(args.seed)

	with open(args.input, 'r') as file:
		_, _, original = cnftools.load(file)
		clauses = list(original)

	comments = [
		'Shuffling of {0:s}'.format(args.input)
	]

	if args.clauses:
		comments.append('Clauses have been shuffled')
		random.shuffle(clauses)

	if args.literals:
		comments.append('Literals within clauses have been shuffled')
		for clause in clauses:
			random.shuffle(clause)

	if args.variables:
		comments.append('Variables have been randomly renamed')

		mapping = cnftools.transform.pack(clauses)
		values = random.sample(list(mapping.values()), k=len(mapping))

		mapping = {k:values[idx] for idx, k in enumerate(mapping.keys())}

		clauses = cnftools.transform.remap(clauses, mapping)

		for literal in sorted(mapping.keys()):
			comments.append('{0:d} -> {1:d}'.format(literal, mapping[literal]))

	with open(args.output, 'w') as file:
		cnftools.dump(clauses, file, comments=comments)
