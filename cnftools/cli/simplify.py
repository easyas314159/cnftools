import cnftools

def add_arguments(subparser):
	parser = subparser.add_parser(
		'simplify',
		description='Simplify a CNF file as much as possible'
	)
	parser.set_defaults(command=main)

	# TODO: Refactor this to allow reading from stdin
	# TODO: Refactor this to allow writing to stdout
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to the Dimacs CNF file to simplify'
	)
	parser.add_argument(
		'-o', '--output',
		type=str,
		required=True,
		help='Path to the resulting simplified CNF'
	)

	parser.add_argument(
		'--imply-units',
		default=False,
		action='store_true',
		help=''
	)

	parser.add_argument(
		'--subsume-clauses',
		default=False,
		action='store_true'
	)

	parser.add_argument(
		'--pure-literals',
		default=False,
		action='store_true'
	)

	return parser

def main(args):
	with open(args.input, 'r') as file:
		_, _, original = cnftools.load(file)
		transformed = list(cnftools.simplify.simplify(
			original,
			imply_units=args.imply_units,
			subsume_clauses=args.subsume_clauses,
			pure_literals=args.pure_literals,
		))

	with open(args.output, 'w') as file:
		cnftools.dump(transformed, file)
