import argparse

from . import threecnf
from . import karps21
from . import simplify
from . import stats

def get_cli_arguments():
	parser = argparse.ArgumentParser()

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands'
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	# CNF to 3-CNF conversion
	threecnf.add_arguments(subparser)

	# CNF statistics
	stats.add_arguments(subparser)

	# CNF simplification tool
	simplify.add_arguments(subparser)

	# Karp's 21 NP-complete problems
	karps21.add_arguments(subparser)

	return parser.parse_args()

def main():
	args = get_cli_arguments()
	exit(args.command(args))

if __name__ == '__main__':
	main()
