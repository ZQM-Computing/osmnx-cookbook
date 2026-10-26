import unittest

import networkx as nx

from examples.graph_from_place import route_summary, validate_graph


class GraphExampleTests(unittest.TestCase):
    def setUp(self):
        self.graph = nx.MultiDiGraph(crs="EPSG:4326")
        self.graph.add_node(1, x=-122.0, y=37.0)
        self.graph.add_node(2, x=-121.999, y=37.0)
        self.graph.add_node(3, x=-121.998, y=37.0)
        self.graph.add_edge(1, 2, length=10.0)
        self.graph.add_edge(2, 3, length=12.0)

    def test_synthetic_graph_is_valid(self):
        validate_graph(self.graph)

    def test_route_summary_uses_nearest_nodes_and_length_weight(self):
        summary = route_summary(self.graph, (-122.0, 37.0), (-121.998, 37.0))
        self.assertEqual(summary["origin_node"], 1)
        self.assertEqual(summary["destination_node"], 3)
        self.assertEqual(summary["node_count"], 3)

    def test_empty_graph_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_graph(nx.MultiDiGraph(crs="EPSG:4326"))


if __name__ == "__main__":
    unittest.main()
