"""Example 01: build a street-network graph for a place.

Two sections, in order:

1. Offline synthetic graph (always runs): a hand-built directed graph
   with 4 nodes and 5 edges, total length 1000 m. This is the part with
   exact expected output, and it needs no network access.
2. Live place query (gated): set OX_DEMO_PLACE to a place query to run
   ox.graph_from_place against Overpass. When unset, this section
   prints a skip message and the script still exits 0 on the strength
   of section 1.

Run with the fleet wave9 Python (OSMnx 2.1.1), by full path, for
example: C:\\geo-tools\\wave9-venv\\Scripts\\python.exe run.py
"""
import os

import networkx as nx
import osmnx as ox

# Synthetic graph: node id -> (x, y). Edge lengths are hand-set metres,
# not computed from coordinates, so the totals below are exact.
NODES = {0: (0.0, 0.0), 1: (0.001, 0.0), 2: (0.0, 0.001), 3: (0.001, 0.001)}
EDGES = [(0, 1, 100), (1, 3, 100), (0, 2, 150), (2, 3, 150), (0, 3, 500)]


def build_synthetic_graph():
    graph = nx.MultiDiGraph(crs="EPSG:4326")
    for node, (x, y) in NODES.items():
        graph.add_node(node, x=x, y=y)
    for u, v, length in EDGES:
        graph.add_edge(u, v, length=length)
    return graph


def main() -> None:
    graph = build_synthetic_graph()
    total = sum(data["length"] for _, _, data in graph.edges(data=True))
    print(f"Synthetic graph: {graph.number_of_nodes()} nodes, "
          f"{graph.number_of_edges()} edges, total length {total} m")
    assert graph.number_of_nodes() == 4
    assert graph.number_of_edges() == 5
    assert total == 1000

    place = os.environ.get("OX_DEMO_PLACE", "")
    if not place:
        print("Live place query skipped: set OX_DEMO_PLACE to a place "
              "query (demo scope pending — see README).")
        return
    live = ox.graph_from_place(place, network_type="drive")
    print(f"Live graph for {place!r}: {live.number_of_nodes()} nodes, "
          f"{live.number_of_edges()} edges")


if __name__ == "__main__":
    main()
