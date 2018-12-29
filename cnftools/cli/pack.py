import sys
import cnftools

from . import cnfio

def add_arguments(subparser):
	parser = subparser.add_parser(
		'pack',
		description='Renumber the literals in a Dimacs CNF file so that they map to 1..N'
	)
	parser.set_defaults(command=main)

	parser.add_argument(
		'-i', '--input',
		type=str,
		default=None,
		help='Path to the Dimacs CNF file to pack. Defaults to stdin'
	)
	parser.add_argument(
		'-o', '--output',
		type=str,
		default=None,
		help='Path to the resulting packed CNF'
	)

	return parser

def main(args):
	with cnfio.open(args.input, sys.stdin, 'r') as file:
		_, _, original = cnftools.load(file)
		original = list(original)

		mapping = cnftools.transform.pack(original)
		transformed = list(cnftools.transform.remap(original, mapping))

	comments = [
		'Repacked literals'
	]
	for literal in sorted(mapping.keys()):
		comments.append('{0:d} -> {1:d}'.format(literal, mapping[literal]))

	with cnfio.open(args.output, sys.stdout, 'w') as file:
		cnftools.dump(transformed, file, comments=comments)
