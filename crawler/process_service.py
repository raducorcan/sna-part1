import json
import networkx as nx
import matplotlib.pyplot as plt
from pyparsing import unicode

from pyvis.network import Network

from network_analysis import print_stats


def open_json(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data


def generate_graph(edges, nodes, parties):
    G = nx.Graph()

    filtered_edges = filter(lambda edge: edge["w"] > 2, edges)
    edge_tuples = map(lambda edge: (edge["n1"], edge["n2"], edge["w"]), filtered_edges)
    node_tuples = map(lambda href: (href, {"name": nodes[href], "party": parties.get(href, "Unknown")}), nodes.keys())

    G.add_nodes_from(node_tuples)
    G.add_weighted_edges_from(edge_tuples)

    return G


def augment_graph(G: nx.Graph):
    for node in G.nodes:
        pass


def clean_file_encoding(file_name):
    with open(file_name, 'r') as file:
        data = unicode(file.read())

    with open(f'encoded_{file_name}', 'w') as file:
        file.write(str(data))


def solve():
    edges = open_json("edges_approved.jsons")
    nodes = open_json("names_approved.jsons")
    parties = open_json("parties_approved.jsons")
    G = generate_graph(edges, nodes, parties)

    augment_graph(G)

    nx.write_gml(G, "legi_approved.gml")

    # net = Network(height=720, width=1400)
    # net.from_nx(G)
    # net.show("legi.html")

    # nx.draw_circular(G)
    # plt.show()
    # print_stats(G)


solve()

# clean_file_encoding("names.jsons")
