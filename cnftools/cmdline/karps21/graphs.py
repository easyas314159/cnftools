import networkx as nx

GENERATOR = {
	'atlas': lambda args: (
		nx.graph_atlas(i=args.index),
		'Graph {index} from the Graph Atlas'.format(index=args.index)
	),
	'balanced_tree': lambda args: (
		nx.balanced_tree(args.r, args.height),
		'{r:d}-ary tree of height {h:d}'.format(r=args.r, h=args.height)
	),
}

def add_graph_arguments(subparser):
	# The graph atlas
	atlas = subparser.add_parser(
		'atlas',
		description="""
		A graph from the Graph Atlas.

		See: Ronald C. Read and Robin J. Wilson, An Atlas of Graphs. Oxford University Press, 1998.
		"""
	)
	atlas.set_defaults(generator=GENERATOR['atlas'])
	atlas.add_argument(
		'-i', '--index',
		type=int,
		required=True,
		help='The index of the graph from the atlas to get. The graph at index 0 is assumed to be the null graph.'
	)

	balanced_tree = subparser.add_parser(
		'balanced_tree',
		description='A perfectly balanced r-ary tree of height h.'
	)
	balanced_tree.set_defaults(generator=GENERATOR['balanced_tree'])
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

