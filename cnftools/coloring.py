from itertools import combinations

def color(graph, chromatic_number):
	literals = {}
	for node in graph.nodes():
		index = chromatic_number * node + 1
		literals[node] = list(range(index, index + chromatic_number))

	for node in graph.nodes():
		yield literals[node]
		yield from [[-u, -v] for u, v in combinations(literals[node], r=2)]

	for node0, node1 in graph.edges():
		yield from [[-l0, -l1] for l0, l1 in zip(literals[node0], literals[node1])]
