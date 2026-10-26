#!/usr/bin/env python3
"""Fetch a drivable OSMnx graph and save portable artifacts."""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import networkx as nx
import osmnx as ox

RETRYABLE_HTTP_STATUSES = {429, 502, 503, 504}


def _http_status(error: Exception) -> int | None:
    response = getattr(error, "response", None)
    status = getattr(response, "status_code", None)
    if status is None:
        status = getattr(error, "status_code", None)
    return status if isinstance(status, int) else None


def graph_from_place_with_retry(place: str, attempts: int = 3) -> nx.MultiDiGraph:
    """Retry only known transient HTTP responses; propagate other failures."""
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    ox.settings.use_cache = True
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            graph = ox.graph_from_place(place, network_type="drive", simplify=True)
            validate_graph(graph)
            return graph
        except Exception as error:
            if _http_status(error) not in RETRYABLE_HTTP_STATUSES or attempt + 1 == attempts:
                raise
            last_error = error
            time.sleep(2**attempt)
    assert last_error is not None
    raise last_error


def validate_graph(graph: nx.MultiDiGraph) -> None:
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        raise ValueError("The downloaded street graph contains no nodes or edges")
    if not graph.graph.get("crs"):
        raise ValueError("The street graph is missing its CRS metadata")


def route_summary(graph: nx.MultiDiGraph, origin: tuple[float, float], destination: tuple[float, float]) -> dict[str, object]:
    """Return a shortest route summary for (longitude, latitude) coordinates."""
    validate_graph(graph)
    origin_node = ox.distance.nearest_nodes(graph, X=origin[0], Y=origin[1])
    destination_node = ox.distance.nearest_nodes(graph, X=destination[0], Y=destination[1])
    route = nx.shortest_path(graph, origin_node, destination_node, weight="length")
    return {"origin_node": origin_node, "destination_node": destination_node, "node_count": len(route)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("place", help="Place query passed to Nominatim/OSMnx")
    parser.add_argument("--output-dir", type=Path, default=Path("build"))
    args = parser.parse_args()

    graph = graph_from_place_with_retry(args.place)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    graphml_path = args.output_dir / "street-network.graphml"
    edges_path = args.output_dir / "street-edges.gpkg"
    ox.save_graphml(graph, filepath=graphml_path)
    _, edges = ox.graph_to_gdfs(graph)
    if edges.empty:
        raise RuntimeError("OSMnx produced an empty edge GeoDataFrame")
    edges.to_file(edges_path, driver="GPKG")
    print(f"Saved {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    print(f"GraphML: {graphml_path}")
    print(f"Edges:   {edges_path}")


if __name__ == "__main__":
    main()
