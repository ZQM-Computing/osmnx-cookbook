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

**Status:** Active, public — seeding. Pattern passes land in follow-up work from fleet-verified setups; the tables below list what is planned, not what is already written.

**What this repository is:** OSMnx patterns — see the table below.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Geospatial developers who analyze streets, routes, and places from OpenStreetMap.

## Prerequisites

- OSMnx in the fleet Python geo environment
- Python 3.11+
- Network access to the Overpass API for live passes

## Patterns (planned)

| # | Example | What it will demonstrate |
|---|---------|--------------------------|
| 01 | `01-graph-from-place` | Building a street-network graph for a place |
| 02 | `02-routing` | Shortest paths and route attributes on the graph |
| 03 | `03-overpass-notes` | Handling transient Overpass overloads with delayed retries |
| 04 | `04-full-workflow` | End-to-end: place → graph → routes → map |

## Repository layout

```text
osmnx-cookbook/
├── examples/          # pattern passes, landing in follow-up work
├── README.md
└── LICENSE
```

## Roadmap

- First pattern pass: the first two table rows
- Second pass: the remaining rows, from fleet-verified setups

## Contributing

A contributing guide lands with the first pattern pass. Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [geopandas-cookbook](https://github.com/ZQM-Computing/geopandas-cookbook) — GeoDataFrame patterns: joins, overlays, and spatial analysis
- [pgrouting-cookbook](https://github.com/ZQM-Computing/pgrouting-cookbook) — Shortest path, driving distance, isochrones, turn restrictions
- [maplibre-cookbook](https://github.com/ZQM-Computing/maplibre-cookbook) — Custom layers, 3D terrain, performance tuning, interactive maps
