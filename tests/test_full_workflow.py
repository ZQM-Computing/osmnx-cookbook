import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import networkx as nx

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "examples" / "04-full-workflow" / "run.py"


def load_workflow_module():
    """Load the example module without executing its CLI entry point."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("osmnx_full_workflow", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FullWorkflowArtifactTests(unittest.TestCase):
    def test_offline_workflow_writes_valid_graphml_and_geojson(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env = os.environ.copy()
            env.pop("OX_DEMO_PLACE", None)
            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                cwd=temp_dir,
                env=env,
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertIn("Live place section skipped", result.stdout)

            output = Path(temp_dir) / "output"
            graph_path = output / "graph.graphml"
            route_path = output / "route.geojson"
            self.assertTrue(graph_path.is_file())
            self.assertTrue(route_path.is_file())

            graph = nx.read_graphml(graph_path)
            self.assertEqual(graph.number_of_nodes(), 4)
            self.assertEqual(graph.number_of_edges(), 5)

            route = json.loads(route_path.read_text(encoding="utf-8"))
            self.assertEqual(route["type"], "Feature")
            self.assertEqual(route["geometry"]["type"], "LineString")
            self.assertEqual(route["properties"]["nodes"], [0, 1, 3])
            self.assertEqual(route["properties"]["length_m"], 200)
            self.assertEqual(route["geometry"]["coordinates"], [[0.0, 0.0], [0.001, 0.0], [0.001, 0.001]])

    def test_route_uses_one_single_source_dijkstra_traversal(self):
        module = load_workflow_module()
        graph = module.build_graph()
        with patch("networkx.single_source_dijkstra", wraps=nx.single_source_dijkstra) as dijkstra:
            path, length = module.shortest_route(graph, 0, 3)

        self.assertEqual(path, [0, 1, 3])
        self.assertEqual(length, 200)
        dijkstra.assert_called_once_with(graph, 0, target=3, weight="length")


if __name__ == "__main__":
    unittest.main()
