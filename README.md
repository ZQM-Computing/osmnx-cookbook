# OSMnx Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A **OSMnx cookbook** for street networks, routing, and OpenStreetMap graphs in Python. Patterns are drawn from the ZQM fleet's OSMnx work, including its street-network graph builds and the transient Overpass 502 overloads that a delayed retry clears. It is intended for Geospatial developers who analyze streets, routes, and places from OpenStreetMap. Validate each pattern against your own data, software versions, and operating environment before adopting it.

## Repository role and status

**Status:** Active, public. Four example directories exist. Offline tests cover synthetic graph routing, prove retries apply only to transient HTTP statuses (429/502/503/504) and network timeouts/connections, and validate the full workflow's GraphML/GeoJSON artifacts; live fleet and external-service validation remains pending.

**What this repository is:** OSMnx patterns — see the table below.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Geospatial developers who analyze streets, routes, and places from OpenStreetMap.

## Prerequisites

- OSMnx 2.1.1 in the fleet wave9 Python environment (`C:\geo-tools\wave9-venv` on Node-1 and Node-3; invoke its `Scripts\python.exe` by full path — bare `python` on Node-1 is the hermes-agent venv and must not be used)
- Network access to the Overpass API for live passes (the offline synthetic-graph sections run without it)

## Patterns

| # | Example | What it demonstrates | Status |
|---|---------|----------------------|--------|
| 01 | [examples/01-graph-from-place](examples/01-graph-from-place) | Building a street-network graph for a place | Code + offline tests; live query pending |
| 02 | [examples/02-routing](examples/02-routing) | Shortest paths and route attributes on the graph | Synthetic graph assertions |
| 03 | [examples/03-overpass-notes](examples/03-overpass-notes) | Handling transient Overpass overloads with delayed retries | Offline retry contracts; live API pending |
| 04 | [examples/04-full-workflow](examples/04-full-workflow) | End-to-end: place → graph → routes → artifacts | Offline GraphML/GeoJSON artifacts tested |

## Repository layout

```text
osmnx-cookbook/
├── examples/
│   ├── 01-graph-from-place/
│   ├── 02-routing/
│   ├── 03-overpass-notes/
│   └── 04-full-workflow/
├── README.md
└── LICENSE
```

## Roadmap

- Code pass: four example directories with offline synthetic-graph and retry tests.
- Validate the transient retry behavior against a controlled Overpass HTTP failure and the live fleet OSMnx 2.1.1 runtime.
- Run the offline workflow on Windows in the fleet virtual environment and compare GraphML/GeoJSON artifacts against the Ubuntu CI output.
- Confirm the live place-query scope, artifact paths, and retry delays against the target environment.

## Contributing

A contributing guide lands with the first pattern pass. Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [geopandas-cookbook](https://github.com/ZQM-Computing/geopandas-cookbook) — GeoDataFrame patterns: joins, overlays, and spatial analysis
- [pgrouting-cookbook](https://github.com/ZQM-Computing/pgrouting-cookbook) — Shortest path, driving distance, isochrones, turn restrictions
- [maplibre-cookbook](https://github.com/ZQM-Computing/maplibre-cookbook) — Custom layers, 3D terrain, performance tuning, interactive maps
