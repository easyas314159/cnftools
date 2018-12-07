"""
"""
from itertools import combinations

import networkx as nx

def chromatic_number(graph, k):
	# TODO: There is probably a better way to handle this
	# FIXME: convert_node_labels_to_integers does not guarantee ordering
	graph = nx.convert_node_labels_to_integers(graph, ordering='sorted')

	literals = {}
	for node in graph.nodes():
		index = k * node + 1
		literals[node] = list(range(index, index + k))

	for node in graph.nodes():
		yield literals[node]
		yield from [[-u, -v] for u, v in combinations(literals[node], r=2)]

	for node0, node1 in graph.edges():
		yield from [[-l0, -l1] for l0, l1 in zip(literals[node0], literals[node1])]

def clique_cover(graph, k):
	yield from chromatic_number(
		graph=nx.complement(graph),
		k=k
	)
