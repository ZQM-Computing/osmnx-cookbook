"""Example 04: end-to-end place -> graph -> routes -> map artifacts.

Offline default (always runs): build the synthetic graph from patterns
01/02, compute the 0->3 route, and write two artifacts under ./output:
graph.graphml (the graph) and route.geojson (the route as a LineString).
No network access, no place query, no plotting dependency.

Live variant (gated): set OX_DEMO_PLACE to a place query to additionally
build a live drive graph with ox.graph_from_place. The live graph's
counts are printed, not asserted — the demo place scope is still an
open question (see pattern 01's README).

Run with the fleet wave9 Python (OSMnx 2.1.1), by full path, for
example: C:\\geo-tools\\wave9-venv\\Scripts\\python.exe run.py
"""
import json
import os
from pathlib import Path

import networkx as nx
import osmnx as ox

NODES = {0: (0.0, 0.0), 1: (0.001, 0.0), 2: (0.0, 0.001), 3: (0.001, 0.001)}
EDGES = [(0, 1, 100), (1, 3, 100), (0, 2, 150), (2, 3, 150), (0, 3, 500)]
OUTPUT_DIR = Path("output")


def build_graph():
    graph = nx.MultiDiGraph(crs="EPSG:4326")
    for node, (x, y) in NODES.items():
        graph.add_node(node, x=x, y=y)
    for u, v, length in EDGES:
        graph.add_edge(u, v, length=length)
    return graph


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    graph = build_graph()
    path = nx.shortest_path(graph, 0, 3, weight="length")
    length = nx.shortest_path_length(graph, 0, 3, weight="length")
    assert path == [0, 1, 3] and length == 200

    nx.write_graphml(graph, OUTPUT_DIR / "graph.graphml")
    route = {
        "type": "Feature",
        "properties": {"nodes": path, "length_m": length, "edges": len(path) - 1},
        "geometry": {
            "type": "LineString",
            "coordinates": [[graph.nodes[n]["x"], graph.nodes[n]["y"]] for n in path],
        },
    }
    (OUTPUT_DIR / "route.geojson").write_text(
        json.dumps(route, indent=2), encoding="utf-8"
    )
    print(f"Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    print(f"Route: {path}, length {length} m")
    print(f"Wrote {OUTPUT_DIR / 'graph.graphml'} and {OUTPUT_DIR / 'route.geojson'}")

    place = os.environ.get("OX_DEMO_PLACE", "")
    if not place:
        print("Live place section skipped: OX_DEMO_PLACE unset (see pattern 01).")
        return
    live = ox.graph_from_place(place, network_type="drive")
    print(f"Live graph for {place!r}: {live.number_of_nodes()} nodes, "
          f"{live.number_of_edges()} edges")


if __name__ == "__main__":
    main()
