from typing import List

import networkx as nx

from data_aquisition.interpreting.domain import LawProject
from jsons.utils import load_from_json


def load_file(file):
    projects_dicts = load_from_json(file)
    result = []
    for project_dict in projects_dicts:
        project = LawProject.from_dict(project_dict)
        result.append(project)

    return result


def generate_nodes(projects: List[LawProject], nodes_accumulator: dict):
    for project in projects:
        for initiator in project.initiators:
            nodes_accumulator[f"{initiator.name} {initiator.party}"] = {
                "name": initiator.name,
                "party": initiator.party,
                "url": initiator.mp
            }


def generate_edges(projects: List[LawProject], edges_accumulator: dict):
    for project in projects:
        count = len(project.initiators)
        for i in range(count):
            for j in range(i + 1, count):
                init1 = project.initiators[i]
                init2 = project.initiators[j]

                name_id1 = f"{init1.name} {init1.party}"
                name_id2 = f"{init2.name} {init2.party}"

                edge_id_lst = [name_id1, name_id2]
                edge_id_lst.sort()
                edge_id = tuple(edge_id_lst)

                if edge_id not in edges_accumulator:
                    edges_accumulator[edge_id] = 0

                edges_accumulator[edge_id] += 1


def generate_graph(files):
    edges, nodes = dict(), dict()
    G = nx.Graph()

    for file in files:
        projects = load_file(file)
        generate_nodes(projects, nodes)
        generate_edges(projects, edges)

    edge_tuples = map(lambda edge_id: (edge_id[0], edge_id[1], edges[edge_id]), edges.keys())  # probably unnecessary
    node_tuples = map(lambda node_id: (node_id, nodes[node_id]), nodes)

    G.add_nodes_from(node_tuples)
    G.add_weighted_edges_from(edge_tuples)

    return G


if __name__ == '__main__':
    years = [2021, 2020, 2019, 2018, 2017, 2016]
    file_names = list(map(lambda year: f'../../data/interpreted/law_projects/all/deputies_{year}.json', years))
    G = generate_graph(file_names)

    nx.write_gml(G, "deputies_2016-2021.gml")
