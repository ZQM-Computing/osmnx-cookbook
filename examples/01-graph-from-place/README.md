# 01 — Graph from place

Build a street-network graph, first offline on a synthetic graph with
exact expected output, then (gated) as a live place query.

## Run

```bash
python run.py
```

Use the fleet wave9 Python by full path
(`C:\geo-tools\wave9-venv\Scripts\python.exe` on Node-1/Node-3); bare
`python` on Node-1 is the hermes-agent venv and must not be used.

## Expected output

Without `OX_DEMO_PLACE` set:

```text
Synthetic graph: 4 nodes, 5 edges, total length 1000 m
Live place query skipped: set OX_DEMO_PLACE to a place query (demo scope pending — see README).
```

The synthetic graph is 4 nodes in a square with a direct diagonal:
edges 0→1 (100 m), 1→3 (100 m), 0→2 (150 m), 2→3 (150 m), 0→3
(500 m). Totals: 5 edges, 100 + 100 + 150 + 150 + 500 = 1000 m.

With `OX_DEMO_PLACE` set, the live section additionally prints the
live graph's node and edge counts. Those counts are **to confirm at
validation** for whatever place is eventually sanctioned as the demo.

## Companion file

This directory also contains `build_graph.py`, a companion
implementation landed separately: it fetches a drivable OSMnx graph
with retries on transient HTTP statuses and saves portable artifacts.
It is not part of this pattern's offline assertions; see that file's
own docstring for its interface.

## Failure behavior

- `OX_DEMO_PLACE` unset: not an error — the live section skips with a
  clear message and the script exits 0 on the synthetic section.
- Live query failing (Overpass overload, bad place string): the
  exception propagates with the place string in the message — see
  pattern 03 for the retry wrapper that belongs around live calls.

## Open question: the demo place

The plan's pattern list requires a place query, but the plan names no
sanctioned demo scope, and the standing no-real-place-data rule
forbids inventing a real-place fixture. The fleet's own wave-9 smoke
queried a real town's drive graph, but naming it here as the demo
would publish a real-place query as the example. Until Alex settles
whether the fleet fixture's place may be named, the live section stays
parameterized behind `OX_DEMO_PLACE` and the runnable core stays
synthetic. Do not fill in a real place name without that call.

## Versions and evidence

- Tool: OSMnx 2.1.1 in the fleet wave9 venv (`C:\geo-tools\wave9-venv`,
  Node-1 and Node-3); networkx ships as OSMnx's graph dependency.
- Evidence level: design-only (gate 1 target). The synthetic section's
  numbers were verified during drafting with an independent Dijkstra
  implementation; the live `graph_from_place` form follows the
  documented OSMnx API and is **to confirm at validation**.
