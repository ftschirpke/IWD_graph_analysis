#!/usr/bin/env python

import argparse
from collections import Counter
import csv
from datetime import datetime
from pathlib import Path
import pickle
import sys
from typing import Dict, List, Tuple, Union

import numpy as np
import networkx as nx

from b_extract_trough_transects import read_graph


def load_obj(name: Union[Path, str]) -> object:
    with open(name, "rb") as f:
        return pickle.load(f)


def add_params_to_graph(G: nx.DiGraph, edge_param_dict: Dict[Tuple, Dict[Tuple, List]]) -> nx.DiGraph:
    """ take entire transect dictionary and
    the original graph G and add the mean/median
    parameter values to the graph edges.

    :param G: trough network graph created
    from skeleton
    :param edge_param_dict: dictionary with
    - key: edge (s, e) and
    - value: list with
        - mean width [m]
        - median width [m]
        - mean depth [m]
        - median depth [m]
        - mean r2
        - median r2
        - ratio of considered transects/trough
        - ratio of water-filled troughs
    :return G_upd: graph with added edge_param_dict
    parameters added as edge weights.
    """
    num_emp = 0
    num_full = 0

    # iterate through all graph edges
    for (s, e) in G.edges():
        # and retrieve information on the corresponding edges from the dictionary
        if (s, e) in edge_param_dict:  # TODO: apparently some (xx) edges aren"t in the edge_param_dict. check out why

            G[s][e]["mean_width"] = edge_param_dict[(s, e)][0]
            G[s][e]["median_width"] = edge_param_dict[(s, e)][1]
            G[s][e]["mean_depth"] = edge_param_dict[(s, e)][2]
            G[s][e]["median_depth"] = edge_param_dict[(s, e)][3]
            G[s][e]["mean_r2"] = edge_param_dict[(s, e)][4]
            G[s][e]["median_r2"] = edge_param_dict[(s, e)][5]
            G[s][e]["considered_trans"] = edge_param_dict[(s, e)][6]
            G[s][e]["water_filled"] = edge_param_dict[(s, e)][7]
            num_full += 1
        else:
            print(f"{str((s, e))} doesn't exist in the edge_param_dict, but only in the Graph.")
            # probably all of the missing ones are those too close to the image border and thus don"t have any transects
            num_emp += 1
    print(f"empty edges: {num_emp}, full edges: {num_full}")
    return G


def analyze_sinks_sources(graph: nx.DiGraph) -> Tuple[int, int]:
    """ analysze how many sources
    and sinks a graph has

    :param graph: an nx.DiGraph
    :return sinks: number of sinks
    :return sources: number of sources
    """
    sinks = 0
    sources = 0
    degree = graph.degree()
    degree_list = []
    for (n, d) in degree:
        degree_list.append(d)
        if graph.in_degree(n) == 0:
            sources += 1
        elif graph.out_degree(n) == 0:
            sinks += 1

    return sinks, sources


def analyze_connected_comp(graph: nx.DiGraph) -> Counter:
    """ print number of connected components
    and their respective sizes """
    graph = graph.to_undirected()
    nodes = []
    edges = []
    node_size = []
    edge_sizes = []

    components = [graph.subgraph(p).copy() for p in nx.connected_components(graph)]
    for comp in components:
        nodes.append(comp.nodes())
        edges.append(comp.edges())

    for c in nx.connected_components(graph):
        node_size.append(len(c))
    for i in edges:
        edge_sizes.append(len(i))

    return Counter(edge_sizes)


def get_network_density(graph) -> Tuple[float, float]:
    """calculate network density of
    graph.

    :param graph: an nx.DiGraph
    :return e_pot: number of potential edges
    :return dens: density of the network
    """
    # number of existing nodes
    num_nodes = nx.number_of_nodes(graph)
    # number of existing edges
    e_exist = nx.number_of_edges(graph)
    # number of potential edges
    e_pot = 3 / 2 * (num_nodes + 1)
    # density
    dens = e_exist / e_pot
    return e_pot, dens


def get_total_channel_length(graph: nx.DiGraph):
    """ calculate the total length of
     all troughs within the study area.

    :param graph: a graph with true
    length of the edge as weight "weight".
    :return l: total length of
    all channels combined.
    """
    total_length = 0
    for (s, e) in graph.edges:
        total_length += graph[s][e]["weight"]
    return round(total_length, 2)


def do_analysis(graph: nx.DiGraph):
    # get sinks and sources
    sinks, sources = analyze_sinks_sources(graph)
    # number of connected components
    connected_comp = analyze_connected_comp(graph)
    # network density
    e_pot, dens = get_network_density(graph)
    # length of all channels in the network
    total_channel_length = get_total_channel_length(graph)
    return graph.number_of_edges(), graph.number_of_nodes(), connected_comp, sinks, sources, e_pot, dens, total_channel_length


def command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("npyFile", type=Path)
    parser.add_argument("edgelistFile", type=Path)
    parser.add_argument("tifFile", type=Path)
    parser.add_argument("dictAvgFile", type=Path)
    parser.add_argument("year", type=str)

    return parser


def main():
    np.set_printoptions(threshold=sys.maxsize)

    parser = command_line_parser()
    args = parser.parse_args()

    # read in 2009 data
    G_09, coord_dict_09 = read_graph(edgelist_loc=args.edgelistFile, coord_dict_loc=args.npyFile)

    transect_dict_fitted_2009: Dict[Tuple, Dict[Tuple, List]] = load_obj(args.dictAvgFile)

    G_upd = add_params_to_graph(G_09, transect_dict_fitted_2009)
    nx.write_edgelist(G_upd, f"arf_graph_{args.year}_avg_weights.edgelist", data=True, delimiter=";")

    number_of_edges, number_of_nodes, connected_comp, sinks, sources, e_pot, dens, total_channel_length = do_analysis(G_09)

    with open(f"graph_{args.tifFile.stem}.csv", "w", newline="") as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow([
            "name", "number_of_edges", "number_of_nodes", "connected_comp", "sinks", "sources",
            "voronoi_edges", "graph_density", "total_channel_length_m"
        ])
        wr.writerow([
            "arf_" + args.tifFile.stem, number_of_edges, number_of_nodes, connected_comp, sinks, sources,
            e_pot, dens, total_channel_length
        ])


if __name__ == "__main__":
    try:
        startTime = datetime.now()
        main()
        print(datetime.now() - startTime)
        sys.exit(0)
    except Exception as ex:
        print(f"Unexpected Error: {ex}")
        sys.exit(1)
