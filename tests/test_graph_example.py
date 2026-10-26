import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

import networkx as nx

MODULE_PATH = Path(__file__).parents[1] / "examples" / "01-graph-from-place" / "build_graph.py"
SPEC = importlib.util.spec_from_file_location("osmnx_example", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
route_summary = MODULE.route_summary
validate_graph = MODULE.validate_graph
graph_from_place_with_retry = MODULE.graph_from_place_with_retry


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


    def test_connection_timeout_retries_then_returns_graph(self):
        with patch.object(MODULE.ox, "graph_from_place", side_effect=[
            requests.exceptions.Timeout("temporary timeout"), self.graph
        ]) as fetch, patch.object(MODULE.time, "sleep") as sleep:
            result = graph_from_place_with_retry("Test Place", attempts=3)
        self.assertIs(result, self.graph)
        self.assertEqual(fetch.call_count, 2)
        sleep.assert_called_once_with(1)

    def test_bad_request_is_not_retried(self):
        error = requests.exceptions.HTTPError("bad request")
        error.response = type("Response", (), {"status_code": 400})()
        with patch.object(MODULE.ox, "graph_from_place", side_effect=error) as fetch:
            with self.assertRaises(requests.exceptions.HTTPError):
                graph_from_place_with_retry("Bad Place", attempts=3)
        fetch.assert_called_once()

    def test_empty_graph_validation_is_not_retried(self):
        with patch.object(MODULE.ox, "graph_from_place", return_value=nx.MultiDiGraph(crs="EPSG:4326")) as fetch:
            with self.assertRaisesRegex(ValueError, "no nodes or edges"):
                graph_from_place_with_retry("Empty Place", attempts=3)
        fetch.assert_called_once()

    def test_retryable_http_502_retries_with_exponential_delays(self):
        error = requests.exceptions.HTTPError("overpass overloaded")
        error.response = type("Response", (), {"status_code": 502})()
        with patch.object(MODULE.ox, "graph_from_place", side_effect=[error, error, self.graph]) as fetch, patch.object(MODULE.time, "sleep") as sleep:
            result = graph_from_place_with_retry("Test Place", attempts=3)
        self.assertIs(result, self.graph)
        self.assertEqual(fetch.call_count, 3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [1, 2])

    def test_attempts_must_be_positive(self):
        with self.assertRaisesRegex(ValueError, "at least 1"):
            graph_from_place_with_retry("Test Place", attempts=0)

    def test_empty_graph_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_graph(nx.MultiDiGraph(crs="EPSG:4326"))


if __name__ == "__main__":
    unittest.main()
