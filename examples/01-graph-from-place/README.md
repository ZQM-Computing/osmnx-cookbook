# Build and validate a street-network graph

This example downloads a drivable street network for a named place, validates that the graph is non-empty, and writes a GraphML artifact plus an edge GeoPackage. It uses OSMnx's cache and a bounded retry for transient Overpass HTTP responses (429, 502, 503, and 504); permanent errors are raised immediately.

## Prerequisites

- Python 3.11 or newer
- Dependencies in `requirements.txt`
- Network access to Nominatim and the configured Overpass endpoint for a live run

## Run

```bash
python examples/01-graph-from-place/build_graph.py "Piedmont, California, USA" --output-dir build
```

The output directory contains `street-network.graphml` and `street-edges.gpkg`. Choose a place appropriate for your project and comply with OpenStreetMap service usage policies. Avoid repeated high-volume requests; cache results and do not use public endpoints as an unlimited production backend.

## Test boundary

Unit tests use a synthetic in-memory graph and do not call geocoding or Overpass. CI therefore verifies route calculations and Python syntax, not live provider availability or the reproducibility of a particular place query.
