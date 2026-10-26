# 02 — Routing

Shortest paths and route attributes on the synthetic graph from
pattern 01. No network access, no place query: every number below is
derived by hand and was checked during drafting with an independent
Dijkstra implementation.

## Run

```bash
python run.py
```

Use the fleet wave9 Python by full path
(`C:\geo-tools\wave9-venv\Scripts\python.exe` on Node-1/Node-3).

## Expected output

```text
Route: [0, 1, 3], length 200 m, edges 2
Cumulative metres along route: [0, 100, 200]
No path from 3 to 0 (expected: graph is directed)
```

Derivation: 0→3 via node 1 costs 100 + 100 = 200 m; via node 2 costs
150 + 150 = 300 m; direct costs 500 m. The minimum is 200 m via
[0, 1, 3]. The reverse direction has no path because every edge in
the synthetic graph points away from node 0's side — the graph is
directed, like a drive network.

## Failure behavior

- A different shortest path or length: the graph builder was edited —
  restore the edge list from `run.py`, do not adjust the assertions.
- `NetworkXNoPath` escaping the `try` block: the directedness
  assumption broke — check that no reverse edges were added.

## Versions and evidence

- Tool: OSMnx 2.1.1 in the fleet wave9 venv; routing uses networkx,
  OSMnx's graph dependency, via the standard `shortest_path` /
  `shortest_path_length` calls with `weight="length"`.
- Evidence level: design-only (gate 1 target). The path, length, and
  cumulative figures were verified during drafting; running them
  against the fleet OSMnx environment is **to confirm at validation**.
