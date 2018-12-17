import cnftools

def add_arguments(subparser):
	parser = subparser.add_parser(
		'pack',
		description='Renumber the literals in a Dimacs CNF file so that they map to 1..N'
	)
	parser.set_defaults(command=main)

	# TODO: Refactor this to allow reading from stdin
	# TODO: Refactor this to allow writing to stdout
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to the Dimacs CNF file to pack'
	)
	parser.add_argument(
		'-o', '--output',
		type=str,
		required=True,
		help='Path to the resulting packed CNF'
	)

	return parser

def main(args):
	with open(args.input, 'r') as file:
		_, _, original = cnftools.load(file)
		original = list(original)

		mapping = cnftools.transform.pack(original)
		transformed = list(cnftools.transform.remap(original, mapping))

	comments = [
		'Repacked literals from {0:s}'.format(args.input)
	]
	for literal in sorted(mapping.keys()):
		comments.append('{0:d} -> {1:d}'.format(literal, mapping[literal]))

	with open(args.output, 'w') as file:
		cnftools.dump(transformed, file, comments=comments)
