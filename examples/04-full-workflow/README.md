# 04 — Full workflow: place → graph → routes → map

Compose patterns 01–03 into one end-to-end pass: build a graph, route
on it, and write map-ready artifacts. The offline default runs
anywhere; the live place section is gated exactly like pattern 01's.

## Run

```bash
python run.py
```

Use the fleet wave9 Python by full path
(`C:\geo-tools\wave9-venv\Scripts\python.exe` on Node-1/Node-3).

## Expected output

```text
Graph: 4 nodes, 5 edges
Route: [0, 1, 3], length 200 m
Wrote output/graph.graphml and output/route.geojson
Live place section skipped: OX_DEMO_PLACE unset (see pattern 01).
```

Artifacts under `./output`:

- `graph.graphml`: the 4-node, 5-edge synthetic graph (readable by
  any GraphML consumer).
- `route.geojson`: one LineString Feature through nodes 0, 1, 3, with
  properties `nodes: [0, 1, 3]`, `length_m: 200`, `edges: 2`. No
  plotting library is required — the GeoJSON is the map artifact,
  ready for any viewer.

With `OX_DEMO_PLACE` set, the live graph's node/edge counts print
after the artifacts. They are reported, not asserted.

## Failure behavior

- Assertion failure on path or length: the graph builder was edited —
  restore the edge list from `run.py`.
- Missing `output/` artifacts: the run died before the writes —
  check the error above the summary lines; do not hand-write the
  artifacts.
- Live section failing: same handling as pattern 01 — wrap live calls
  in pattern 03's retry wrapper for production use; this example keeps
  the live call bare so the gating is visible.

## Versions and evidence

- Tool: OSMnx 2.1.1 in the fleet wave9 venv (Node-1 and Node-3);
  GraphML via networkx, GeoJSON via the standard library.
- Evidence level: design-only (gate 1 target). The offline section's
  numbers match patterns 01/02 exactly; the live section and any
  viewer rendering are **to confirm at validation**.
