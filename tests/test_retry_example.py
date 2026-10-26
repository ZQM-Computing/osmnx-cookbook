import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "examples" / "03-overpass-notes" / "run.py"
SPEC = importlib.util.spec_from_file_location("osmnx_retry_example", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RetryExampleTests(unittest.TestCase):
    def test_transient_502_retries_then_succeeds(self):
        fetcher = MODULE.FlakyFetcher(2)
        value, attempts = MODULE.fetch_with_retry(fetcher, delays=(0, 0))
        self.assertEqual((value, attempts), ("OK", 3))
        self.assertEqual(fetcher.calls, 3)

    def test_permanent_exception_propagates_without_retry(self):
        calls = 0

        def fetch():
            nonlocal calls
            calls += 1
            raise ValueError("invalid query")

        with self.assertRaisesRegex(ValueError, "invalid query"):
            MODULE.fetch_with_retry(fetch, delays=(0, 0))
        self.assertEqual(calls, 1)

    def test_non_retryable_http_status_is_not_retried(self):
        calls = 0

        class Response:
            status_code = 400

        class BadRequest(RuntimeError):
            response = Response()

        def fetch():
            nonlocal calls
            calls += 1
            raise BadRequest("bad query")

        with self.assertRaisesRegex(BadRequest, "bad query"):
            MODULE.fetch_with_retry(fetch, delays=(0, 0))
        self.assertEqual(calls, 1)

    def test_retryable_failures_stop_after_configured_attempts(self):
        fetcher = MODULE.FlakyFetcher(10)
        with self.assertRaisesRegex(RuntimeError, "after 3 attempts"):
            MODULE.fetch_with_retry(fetcher, delays=(0, 0))
        self.assertEqual(fetcher.calls, 3)


if __name__ == "__main__":
    unittest.main()
