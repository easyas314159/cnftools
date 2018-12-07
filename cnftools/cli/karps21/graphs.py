import networkx as nx

def add_graph_arguments(subparser):
	generators = [
		atlas, balanced_tree, adjlist
	]

	for generator in generators:
		generator(subparser)

	return subparser

def atlas(subparser):
	"""Initialize command-line arguments and generators for the Graph Atlas
	"""
	parser = subparser.add_parser(
		'atlas',
		description="""
		A graph from the Graph Atlas.

		See: Ronald C. Read and Robin J. Wilson, An Atlas of Graphs. Oxford University Press, 1998.
		"""
	)

	parser.add_argument(
		'-i', '--index',
		type=int,
		required=True,
		help='The index of the graph from the atlas to get. The graph at index 0 is assumed to be the null graph.'
	)

	def generate(args):
		return nx.graph_atlas(i=args.index)
	def describe(args):
		return 'Graph {index} from the Graph Atlas'.format(index=args.index)

	parser.set_defaults(generate=generate, describe=describe)

	return parser

def balanced_tree(subparser):
	"""Initialize command-line arguments and generators for balanced trees
	"""

	parser = subparser.add_parser(
		'balanced_tree',
		description='A perfectly balanced r-ary tree of height h.'
	)

	parser.add_argument(
		'-r',
		type=int,
		required=True,
		help='Branching factor of the tree; each node will this many children.'
	)
	parser.add_argument(
		'--height',
		type=int,
		required=True,
		help='Height of the tree.'
	)

	def generate(args):
		return nx.balanced_tree(args.r, args.height)
	def describe(args):
		return '{r:d}-ary tree of height {h:d}'.format(r=args.r, h=args.height)

	parser.set_defaults(generate=generate, describe=describe)

	return parser

# NetworkX graph file loaders

def adjlist(subparser):
	"""Initialize command-line arguments and generators for loading adjaceny lists
	"""
	parser = subparser.add_parser(
		'adjlist',
		description="""
		Read an adjacency list from file.
		"""
	)
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to adjacency list file'
	)

	def generate(args):
		return nx.read_adjlist(args.input)
	def describe(args):
		return 'Adjacency list loaded from {input:s}'.format(input=args.input)

	parser.set_defaults(generate=generate, describe=describe)

	return parser
