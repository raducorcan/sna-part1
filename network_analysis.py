import networkx as nx
import collections
import matplotlib.pyplot as plt
from pyvis.network import Network


def counter_scatter_plot(values, *, title="Title", plot_type=plt.loglog, repr_type="go"):
    value_counts = collections.Counter(values)
    value_counts = sorted(value_counts.items())
    x, y = zip(*value_counts)
    plot_type(x, y, repr_type)
    plt.title(title)
    plt.show()


def best_nodes(graph: nx.Graph):
    betwn_centr = nx.betweenness_centrality(graph)
    best_betwn_centr = max(betwn_centr, key=lambda x: betwn_centr[x])
    print(
        f"Most important node according to betweenness centrality is node {graph.nodes[best_betwn_centr]['label']} with betweenness centrality {betwn_centr[best_betwn_centr]}")
    graph.nodes[best_betwn_centr]['color'] = 'green'

    close_centr = nx.closeness_centrality(graph)
    best_close_centr = max(close_centr, key=lambda x: close_centr[x])
    print(
        f"Most important node according to closeness centrality is node {graph.nodes[best_close_centr]['label']} with closeness centrality {close_centr[best_close_centr]}")
    graph.nodes[best_close_centr]['color'] = 'yellow'

    deg_centr = nx.degree_centrality(graph)
    best_deg_centr = max(deg_centr, key=lambda x: deg_centr[x])
    print(
        f"Most important node according to degree centrality is node {graph.nodes[best_deg_centr]['label']} with degree centrality {deg_centr[best_deg_centr]}")
    graph.nodes[best_deg_centr]['color'] = 'magenta'

    eigen_centr = nx.eigenvector_centrality(graph)
    best_eigen_centr = max(eigen_centr, key=lambda x: eigen_centr[x])
    print(
        f"Most important node according to eigenvector centrality is node {graph.nodes[best_eigen_centr]['label']} with eigenvector  centrality {eigen_centr[best_eigen_centr]}")
    graph.nodes[best_eigen_centr]['color'] = 'red'


def plot_distributions(graph):
    degs = list(map(lambda x: x[1], nx.degree(graph)))
    counter_scatter_plot(degs, title="Degree distribution")

    clus_coefs = nx.clustering(graph).values()
    counter_scatter_plot(clus_coefs, title="Clustering coefficient distribution")

    betwn_centr = nx.betweenness_centrality(graph).values()
    counter_scatter_plot(betwn_centr, title="Betweenness centrality distribution")

    comp_lens = [len(comp) for comp in nx.connected_components(graph)]
    counter_scatter_plot(comp_lens, title="Connected components size distribution")

    max_conn = graph.subgraph(max(nx.connected_components(graph), key=len))
    dists = []
    for el in nx.shortest_path_length(max_conn):
        src, dict = el
        dists.extend(dict.values())
    counter_scatter_plot(dists, title="Distances distribution", plot_type=plt.plot, repr_type='g-')


def print_stats(graph):
    nodes = len(nx.nodes(graph))
    print(f"Number of nodes: {nodes}")
    print(f"Number of edges: {len(nx.edges(graph))}")

    degs = list(map(lambda x: x[1], nx.degree(graph)))
    print(f"Min degree: {min(degs)}")
    print(f"Max degree: {max(degs)}")
    print(f"Average degree: {sum(degs) / len(degs)}")
    print(f"Average clustering coefficient: {nx.average_clustering(graph)}")

    print(f"Graph has {len(list(nx.connected_components(graph)))} connected component(s)")
    print("--------------------")
    print(f"The largest component has {len(max(nx.connected_components(graph), key=len))} nodes")

    max_conn = graph.subgraph(max(nx.connected_components(graph), key=len))
    print(f"Its diameter is {nx.diameter(max_conn)}")
    plot_distributions(graph)
    best_nodes(graph)
    print("--------------------GRAPH END--------------------")


def run():
    graph = nx.read_gml("./res/netscience.gml", label="id")
    nodes = len(nx.nodes(graph))

    # er_graph = nx.fast_gnp_random_graph(nodes, 0.0025)  # random graph using Erdos-Renyi model
    # ba_graph = nx.barabasi_albert_graph(nodes, 2)  # random graph using Barabasi-Albert model

    print_stats(graph)
    # print_stats(er_graph)
    # print_stats(ba_graph)

    # network visualisation

    # net = Network(height=720, width=1400)
    # net.from_nx(graph)
    # net.show("netscience.html")


run()
