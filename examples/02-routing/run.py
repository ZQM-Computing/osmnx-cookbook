"""Example 02: shortest paths and route attributes on the synthetic graph.

Same hand-built graph as pattern 01: 4 nodes, directed edges
0->1 (100 m), 1->3 (100 m), 0->2 (150 m), 2->3 (150 m), 0->3 (500 m).
Shortest path 0->3 is [0, 1, 3] at 200 m (via node 1 beats 300 m via
node 2 and 500 m direct). The graph is directed, so 3->0 has no path.

Run with the fleet wave9 Python (OSMnx 2.1.1), by full path, for
example: C:\\geo-tools\\wave9-venv\\Scripts\\python.exe run.py
"""
import networkx as nx

NODES = {0: (0.0, 0.0), 1: (0.001, 0.0), 2: (0.0, 0.001), 3: (0.001, 0.001)}
EDGES = [(0, 1, 100), (1, 3, 100), (0, 2, 150), (2, 3, 150), (0, 3, 500)]


def build_graph():
    graph = nx.MultiDiGraph(crs="EPSG:4326")
    for node, (x, y) in NODES.items():
        graph.add_node(node, x=x, y=y)
    for u, v, length in EDGES:
        graph.add_edge(u, v, length=length)
    return graph


def main() -> None:
    graph = build_graph()
    path = nx.shortest_path(graph, 0, 3, weight="length")
    length = nx.shortest_path_length(graph, 0, 3, weight="length")
    cumulative = [0]
    for u, v in zip(path, path[1:]):
        cumulative.append(cumulative[-1] + graph[u][v][0]["length"])
    print(f"Route: {path}, length {length} m, edges {len(path) - 1}")
    print(f"Cumulative metres along route: {cumulative}")
    assert path == [0, 1, 3] and length == 200
    assert cumulative == [0, 100, 200]
    try:
        nx.shortest_path(graph, 3, 0, weight="length")
    except nx.NetworkXNoPath:
        print("No path from 3 to 0 (expected: graph is directed)")
    else:
        raise SystemExit("Expected no path from 3 to 0")


if __name__ == "__main__":
    main()
