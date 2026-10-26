# 03 — Overpass notes: delayed retries

Handle the transient Overpass failure the fleet actually hit: 502
"request queue is full", twice, then success after a delay — on both
Node-1 and Node-3 wave-9 OSMnx graph builds.

## Run

```bash
python run.py
```

Use the fleet wave9 Python by full path
(`C:\geo-tools\wave9-venv\Scripts\python.exe` on Node-1/Node-3). The
demo uses fake fetchers and (0, 0) delays, so it finishes instantly
with no network. Set `OX_RETRY_DEMO=live` to run it with the live
delays (30 s, then 120 s).

## Expected output

```text
Flaky fetch: OK after 3 attempts
Dead fetch: Fetch failed after 3 attempts: Overpass 502 "request queue is full"
```

The wrapper's rule: attempts = delays + 1. Two delays give three
attempts, matching the fleet shape (two failures, third succeeds).

## Failure behavior

- All retries exhausted: the wrapper raises `RuntimeError` naming the
  attempt count and the last error — that is the designed outcome,
  not a crash to paper over. A persistent 502 across all attempts
  means upstream is still overloaded or the query is too large; shrink
  the query (pattern 01's smallest-query rule) and retry later.
- Instant success on the first attempt in production: fine — the
  wrapper is a no-op when nothing fails.

## Notes and open questions

- The delays (30 s, 120 s) are starting values, not fleet-measured
  numbers: the fleet record proves only the shape (two 502s, then
  success after a delay), not the seconds. Tuning them against live
  Overpass behavior is **to confirm at validation**.
- Keep queries small: the fleet lesson is that overload is transient
  for small queries. Never bulk-download through this wrapper to
  work around rate limits — that turns a transient-overload retry
  into abusive load.
- OSMnx timeout/endpoint settings (for example `ox.settings.timeout`)
  are the adjacent knobs for slow-but-not-failing queries; their exact
  spellings are **to confirm at validation**.

## Versions and evidence

- Tool: OSMnx 2.1.1 in the fleet wave9 venv (Node-1 and Node-3).
- Evidence level: design-only (gate 1 target). The retry wrapper and
  both demo paths are deterministic and were executed during
  drafting; the live delays and settings spellings are validation
  items.
