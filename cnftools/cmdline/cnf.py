import argparse

from cnftools import cmdline

def get_cli_arguments():
	parser = argparse.ArgumentParser()

	subparser = parser.add_subparsers(
		title='Sub-commands',
		description='Available sub-commands',
		required=True
	)

	# CNF to 3-CNF conversion
	cmdline.threecnf.add_arguments(subparser)

	# Karp's 21 NP-complete problems
	cmdline.karps21.add_arguments(subparser)

	return parser.parse_args()

def main():
	args = get_cli_arguments()
	exit(args.command(args))
