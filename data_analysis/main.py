from data_aquisition.grapher.grapher import generate_graph
from networkx.algorithms import community, nx


def get_graph():
    return nx.read_gml('deputies_2016-2021.gml')


if __name__ == '__main__':
    G = get_graph()

    connected = G.subgraph(max(nx.connected_components(G), key=len))
    communities = community.asyn_fluidc(connected, 6, max_iter=1000, seed=123123)

    for index, community in enumerate(communities):
        hist = {}
        for node_id in community:
            party = G.nodes[node_id]["party"]
            G.nodes[node_id]["community_id"] = index

            if party not in hist:
                hist[party] = 0

            hist[party] += 1

        print(f"Community {index}:")
        for party in hist.keys():
            print(f"{party}: {hist[party]}")
        print("\n")

    nx.write_gml(G, "deputies_2016-2021_asyn_fluid.gml")
