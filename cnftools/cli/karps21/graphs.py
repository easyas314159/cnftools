import networkx as nx

def add_graph_arguments(subparser):
	generators = [
		atlas, balanced_tree,
		adjlist, gexf, graphml, yaml,
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
# TODO: Can these loader be parameterized?

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

def gexf(subparser):
	"""Initialize command-line arguments and generators for loading Graph Exchange XML Format.
	"""
	parser = subparser.add_parser(
		'gexf',
		description="""
		Read a Graph Exchange XML Format file.
		"""
	)
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to GEXF file.'
	)

	def generate(args):
		return nx.read_gexf(args.input)
	def describe(args):
		return 'Graph Exchange XML Format loaded from {input:s}'.format(input=args.input)

	parser.set_defaults(generate=generate, describe=describe)

	return parser

def graphml(subparser):
	"""Initialize command-line arguments and generators for loading GraphML.
	"""
	parser = subparser.add_parser(
		'graphml',
		description="""
		Read a GraphML file.
		"""
	)
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to GraphML file.'
	)

	def generate(args):
		return nx.read_graphml(args.input)
	def describe(args):
		return 'GraphML loaded from {input:s}'.format(input=args.input)

	parser.set_defaults(generate=generate, describe=describe)

	return parser

def yaml(subparser):
	"""Initialize command-line arguments and generators for loading YAML.
	"""
	parser = subparser.add_parser(
		'yaml',
		description="""
		Read a YAML file.
		"""
	)
	parser.add_argument(
		'-i', '--input',
		type=str,
		required=True,
		help='Path to YAML file.'
	)

	def generate(args):
		return nx.read_yaml(args.input)
	def describe(args):
		return 'YAML loaded from {input:s}'.format(input=args.input)

	parser.set_defaults(generate=generate, describe=describe)

	return parser
