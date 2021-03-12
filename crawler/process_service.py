import json
import networkx as nx
import matplotlib.pyplot as plt

from pyvis.network import Network

from network_analysis import print_stats


def open_json(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data


def generate_graph(edges, nodes):
    G = nx.Graph()

    filtered_edges = filter(lambda  edge: edge["w"] > 2, edges)
    edge_tuples = map(lambda edge: (edge["n1"], edge["n2"], edge["w"]), filtered_edges)
    node_tuples = map(lambda href: (href, {"label": nodes[href]}), nodes.keys())

    G.add_nodes_from(node_tuples)
    G.add_weighted_edges_from(edge_tuples)

    return G


def solve():
    edges = open_json("edges.json")
    nodes = open_json("names.json")
    G = generate_graph(edges, nodes)

    # net = Network(height=720, width=1400)
    # net.from_nx(G)
    # net.show("legi.html")

    nx.draw_circular(G)
    plt.show()
    # print_stats(G)


solve()
