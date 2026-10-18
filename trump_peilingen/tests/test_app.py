import unittest
from unittest.mock import patch

import polls
from app import app
from polls import PollingDataError, PollingSnapshot, parse_polling_page


SAMPLE_PAGE = """
<html>
  <head><title>Donald Trump Approval Rating Polling Average | DDHQ</title></head>
  <body>
    <h1>Donald Trump Approval Rating</h1>
    <div>Response Disapprove 55.25%</div>
    <div>Response Approve 41.50%</div>
  </body>
</html>
"""


class PollingPageTests(unittest.TestCase):
    def test_parses_approval_and_disapproval_percentages(self):
        self.assertEqual(parse_polling_page(SAMPLE_PAGE), (41.5, 55.25))

    def test_rejects_a_page_without_trump_approval_data(self):
        with self.assertRaises(PollingDataError):
            parse_polling_page("<html><body>No polling data</body></html>")

    def test_rejects_out_of_range_percentages(self):
        page = SAMPLE_PAGE.replace("55.25%", "155.25%")
        with self.assertRaises(PollingDataError):
            parse_polling_page(page)


class PollingCacheTests(unittest.TestCase):
    def setUp(self):
        polls._cached_snapshot = None
        polls._cached_at = 0.0

    def tearDown(self):
        polls._cached_snapshot = None
        polls._cached_at = 0.0

    @patch("polls.fetch_polling_snapshot")
    def test_reuses_cached_snapshot_until_refresh_is_requested(self, fetch):
        expected = PollingSnapshot(41.5, 55.25, polls.datetime.now().astimezone())
        fetch.return_value = expected

        self.assertIs(polls.get_polling_snapshot(), expected)
        self.assertIs(polls.get_polling_snapshot(), expected)
        self.assertEqual(fetch.call_count, 1)

        self.assertIs(polls.get_polling_snapshot(force_refresh=True), expected)
        self.assertEqual(fetch.call_count, 2)


class AppRouteTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    @patch("app.get_polling_snapshot")
    def test_homepage_displays_approval_and_net_approval(self, get_snapshot):
        get_snapshot.return_value = PollingSnapshot(
            41.5, 55.25, polls.datetime.now().astimezone()
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"41.5", response.data)
        self.assertIn(b"55.2", response.data)
        self.assertIn(b"-13.8", response.data)

    @patch("app.get_polling_snapshot", side_effect=PollingDataError("Bron niet bereikbaar."))
    def test_homepage_reports_polling_source_errors(self, _get_snapshot):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 502)
        self.assertIn("Bron niet bereikbaar.".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
