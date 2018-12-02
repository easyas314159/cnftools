#!/usr/bin/env python
import argparse

import networkx as nx

import cnftools

GENERATOR = {
	'atlas': lambda args: (
		nx.graph_atlas(i=args.index),
		'{k:d}-coloring of graph {index} from the Graph Atlas'.format(k=args.k, index=args.index)
	),
	'balanced_tree': lambda args: (
		nx.balanced_tree(args.r, args.height),
		'{k:d}-coloring of a {r:d}-ary tree of height {h:d}'.format(k=args.k, r=args.r, h=args.height)
	),
}

def get_cli_arguments():
	parser = argparse.ArgumentParser()

	general = parser.add_argument_group('General settings')
	general.add_argument(
		'-k',
		type=int,
		required=True,
		help='The target chromatic number of the graph'
	)
	# TODO: Add support for writing to stdout
	general.add_argument(
		'-o', '--output',
		type=str,
		required=True,
		help=''
	)

	subparsers = parser.add_subparsers(dest='generator', required=True, help='Sub-command Help')

	# The graph atlas
	atlas = subparsers.add_parser(
		'atlas',
		description="""
		A graph from the Graph Atlas.

		See: Ronald C. Read and Robin J. Wilson, An Atlas of Graphs. Oxford University Press, 1998.
		"""
	)
	atlas.add_argument(
		'-i', '--index',
		type=int,
		required=True,
		help='The index of the graph from the atlas to get. The graph at index 0 is assumed to be the null graph.'
	)

	balanced_tree = subparsers.add_parser(
		'balanced_tree',
		description="""
		A perfectly balanced r-ary tree of height h.
		"""
	)
	balanced_tree.add_argument(
		'-r',
		type=int,
		required=True,
		help='Branching factor of the tree; each node will this many children.'
	)
	balanced_tree.add_argument(
		'--height',
		type=int,
		required=True,
		help='Height of the tree.'
	)

	return parser.parse_args()

def main():
	args = get_cli_arguments()

	graph, comment = GENERATOR[args.generator](args)
	clauses = cnftools.color(graph, args.k)

	with open(args.output, 'w') as file:
		cnftools.dump(clauses, file, comment=comment)

if __name__ == '__main__':
	main()
