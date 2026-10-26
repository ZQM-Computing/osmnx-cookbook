"""Example 03: delayed retries around transient Overpass overloads.

Fleet evidence: OSMnx graph builds on Node-1 and Node-3 each hit
Overpass 502 "request queue is full" twice, then succeeded after a
delay. This pattern wraps any fetch callable in that shape: retry on
failure, wait between attempts, and fail loudly only when the retries
are exhausted.

The demo runs against fake fetchers (no network) so the retry behavior
is deterministic: one fetcher fails twice then succeeds; one always
fails. Live defaults are deliberately slow (30 s, then 120 s); the demo
passes (0, 0) delays so it finishes instantly. Set OX_RETRY_DEMO=live
to run the demo with the live delays.

Run with the fleet wave9 Python (OSMnx 2.1.1), by full path, for
example: C:\\geo-tools\\wave9-venv\\Scripts\\python.exe run.py
"""
import os
import time


def fetch_with_retry(fetch, delays=(30, 120)):
    """Call fetch(); on exception, sleep through delays, then retry.

    Returns fetch()'s value on the first success. Raises the last
    exception once delays are exhausted. Total attempts = len(delays)+1.
    """
    attempts = 0
    while True:
        attempts += 1
        try:
            return fetch(), attempts
        except Exception as exc:  # noqa: BLE001 - retry wrapper, re-raised below
            if attempts > len(delays):
                raise RuntimeError(
                    f"Fetch failed after {attempts} attempts: {exc}"
                ) from exc
            time.sleep(delays[attempts - 1])


class FlakyFetcher:
    """Fails fail_times times with a 502-style error, then succeeds."""

    def __init__(self, fail_times):
        self.remaining = fail_times
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self.remaining > 0:
            self.remaining -= 1
            raise RuntimeError('Overpass 502 "request queue is full"')
        return "OK"


def main() -> None:
    live = os.environ.get("OX_RETRY_DEMO", "") == "live"
    delays = (30, 120) if live else (0, 0)
    flaky = FlakyFetcher(2)
    value, attempts = fetch_with_retry(flaky, delays)
    print(f"Flaky fetch: {value} after {attempts} attempts")
    assert (value, attempts) == ("OK", 3)

    dead = FlakyFetcher(99)
    try:
        fetch_with_retry(dead, delays)
    except RuntimeError as exc:
        print(f"Dead fetch: {exc}")
        assert "after 3 attempts" in str(exc)
    else:
        raise SystemExit("Expected the dead fetch to raise")


if __name__ == "__main__":
    main()
