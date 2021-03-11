import networkx as nx
import collections
import matplotlib.pyplot as plt
from pyvis.network import Network


# def save_sub_graph(graph):
#     graph = nx.subgraph(graph, list(range(1, 1001)))
#     nx.write_gml(graph, "./res/netscience.gml")

def counter_scatter_plot(values, *, title="Title", plot_type=plt.loglog):
    value_counts = collections.Counter(values)
    value_counts = sorted(value_counts.items())
    x, y = zip(*value_counts)
    plot_type(x, y, 'go')
    plt.title(title)
    plt.show()


def plot_distributions(graph):
    degs = list(map(lambda x: x[1], nx.degree(graph)))
    counter_scatter_plot(degs, title="Degree distribution")

    clus_coefs = nx.clustering(graph).values()
    counter_scatter_plot(clus_coefs, title="Clustering coefficient distribution")

    betwn_centr = nx.betweenness_centrality(graph).values()
    counter_scatter_plot(betwn_centr, title="Betweenness centrality distribution")

    comp_lens = [len(comp) for comp in nx.connected_components(graph)]
    print(max(nx.connected_components(graph)))
    counter_scatter_plot(comp_lens, title="Connected components size distribution")


def print_stats(graph):
    nodes = len(nx.nodes(graph))
    print(f"Number of nodes: {nodes}")
    print(f"Number of edges: {len(nx.edges(graph))}")

    degs = list(map(lambda x: x[1], nx.degree(graph)))
    print(f"Min degree: {min(degs)}")
    print(f"Max degree: {max(degs)}")
    print(f"Average degree: {sum(degs) / len(degs)}")
    print(f"Average clustering coefficient: {nx.average_clustering(graph)}")
    # print(f"Diameter: {nx.diameter(graph)}")

    print(f"Graph has {len(list(nx.connected_components(graph)))} connected component(s)")
    plot_distributions(graph)
    print("------------------------------------------")


def run():
    graph = nx.read_gml("./res/netscience.gml", label="id")
    nodes = len(nx.nodes(graph))
    # er_graph = nx.fast_gnp_random_graph(nodes, 0.0025)
    # ba_graph = nx.barabasi_albert_graph(nodes, 2)

    # print_stats(graph)
    # print_stats(er_graph)
    # print_stats(ba_graph)

    net = Network(height=720, width=1400)
    net.from_nx(graph)
    net.show("netscience.html")

run()
