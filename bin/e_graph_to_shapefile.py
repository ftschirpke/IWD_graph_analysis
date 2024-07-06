#!/usr/bin/env python

import argparse
import ast
import csv
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict

import fiona
from geopandas import GeoDataFrame
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point

from b_extract_trough_transects import read_graph


def create_point_shp_nodes(coord_dict: Dict, save_loc_shp: str):
    # define schema
    schema_pts = {
        "geometry": "Point",
        "properties": [("ID", "int")]
    }
    # open a fiona object
    node_shp = fiona.open(save_loc_shp, mode="w", driver="ESRI Shapefile", schema=schema_pts)

    # iterate over each row in the dataframe and save record
    for key, value in coord_dict.items():
        row_dict = {
            "geometry": {"type": "Point",
                         "coordinates": (value[0], value[1])},
            "properties": {"ID": key},
        }
        node_shp.write(row_dict)
    # close fiona object
    node_shp.close()


def get_edge_info_csv(weighted_graph: Path, csv_loc: str):
    with open(weighted_graph) as graph_file, open(csv_loc, "w", newline="") as f:
        reader = csv.reader(graph_file, delimiter=";")
        writer = csv.writer(f)

        header = [
            "start_node", "end_node", "pts", "length", "mean_width", "median_width",
            "mean_depth", "median_depth", "mean_r2", "median_r2",
            "considered_trans", "water_filled"
        ]
        writer.writerow(header)
        for row in reader:
            thisrow = []
            thisrow.append(row[0])
            thisrow.append(row[1])
            row_as_string = row[2]
            row_as_string = row_as_string.replace("nan", "\"NULL\"")
            dicti = ast.literal_eval(row_as_string)
            vals = list(dicti.values())
            for i in list(range(len(vals))):
                thisrow.append(vals[i])
            writer.writerow(thisrow)


def add_coords_to_edge_id(csv: str, coord_dict: Dict) -> pd.DataFrame:
    edge_info = pd.read_csv(csv)

    start_lat = []
    start_lon = []
    end_lat = []
    end_lon = []
    geometry = []

    # iterate through starting nodes and grab coordinates from dictionary
    for edge in edge_info["start_node"]:
        start_lat.append(int(coord_dict[str(edge)][0]))
        start_lon.append(int(coord_dict[str(edge)][1]))
    # iterate through ending nodes and grab coordinates from dictionary
    for edge in edge_info["end_node"]:
        end_lat.append(int(coord_dict[str(edge)][0]))
        end_lon.append(int(coord_dict[str(edge)][1]))

    for row in range(len(edge_info)):
        geometry.append(LineString([Point(start_lat[row], start_lon[row]), Point(end_lat[row], end_lon[row])]))

    # add the coordinates to the dataframe
    edge_info["start_lat"] = start_lat
    edge_info["start_lon"] = start_lon
    edge_info["end_lat"] = end_lat
    edge_info["end_lon"] = end_lon
    edge_info["geometry"] = geometry

    # output the dataframe so a shapefile can be built from it after
    return edge_info


def create_line_shp_edges(edge_info_df: pd.DataFrame, save_loc_shp: str):
    edge_info_gdf = GeoDataFrame(edge_info_df, geometry=edge_info_df["geometry"])
    edge_info_gdf.to_file(save_loc_shp, mode="w", driver="ESRI Shapefile")


def command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("npyFile", type=Path)
    parser.add_argument("edgelistFile", type=Path)
    parser.add_argument("weightedGraphFile", type=Path)

    return parser


def main():
    pd.set_option("display.max_columns", None)
    np.set_printoptions(threshold=sys.maxsize)

    parser = command_line_parser()
    args = parser.parse_args()

    # read in 2009 datagraph_2009.csv
    G, coord_dict = read_graph(edgelist_loc=args.edgelistFile, coord_dict_loc=args.npyFile)
    print(args.edgelistFile)
    aoiName = args.edgelistFile.stem

    # generate point-shapefile from nodes.
    create_point_shp_nodes(coord_dict, f"{aoiName}_nodes.shp")

    # prepare for shapefiling edges
    get_edge_info_csv(args.weightedGraphFile, f"{aoiName}_edges_csv.csv")

    # shapefile edges
    edge_info_df = add_coords_to_edge_id(f"{aoiName}_edges_csv.csv", coord_dict)
    create_line_shp_edges(edge_info_df, f"{aoiName}_edges.shp")


if __name__ == "__main__":
    try:
        startTime = datetime.now()
        main()
        print(datetime.now() - startTime)
        sys.exit(0)
    except Exception as ex:
        print(f"Unexpected Error: {ex}")
        sys.exit(1)
