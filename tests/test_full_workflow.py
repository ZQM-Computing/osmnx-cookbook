import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "examples" / "04-full-workflow" / "run.py"


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


if __name__ == "__main__":
    unittest.main()
