import argparse

from . import threecnf
from . import karps21
from . import simplify
from . import stats
from . import pack
from . import shuffle

def get_cli_arguments():
	parser = argparse.ArgumentParser()

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands'
	)
	# Work around https://bugs.python.org/issue9253
	subparser.required = True

	utilities = [
		stats, pack, shuffle, threecnf, simplify, karps21
	]

	for utility in utilities:
		utility.add_arguments(subparser)

	return parser.parse_args()

def main():
	args = get_cli_arguments()
	exit(args.command(args))

if __name__ == '__main__':
	main()
