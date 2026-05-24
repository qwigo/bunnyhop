"""
Tests for stats.py and billing.py — written TDD-style so they FAIL against the
broken code and PASS after the fixes described in issues C2 and M8.
"""
import collections
import collections.abc
import unittest
from unittest.mock import patch, MagicMock

# valley 1.5.5 uses collections.Callable which was removed in Python 3.10+.
# Restore the alias before any bunnyhop imports so the library can initialise.
if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable


STATS_RESPONSE = {
    "TotalBandwidthUsed": 123456,
    "TotalRequestsServed": 789,
    "CacheHitRate": 0.95,
    "BandwidthUsedChart": {},
    "BandwidthCachedChart": {},
    "CacheHitRateChart": {},
    "RequestsServedChart": {},
    "PullRequestsPulledChart": {},
    "OriginShieldBandwidthUsedChart": {},
    "OriginShieldInternalBandwidthUsedChart": {},
    "UserBalanceHistoryChart": {},
    "GeoTrafficDistribution": {},
    "Error3xxChart": {},
    "Error4xxChart": {},
    "Error5xxChart": {},
}

BILLING_SUMMARY_RESPONSE = {
    "Balance": 10.0,
    "ThisMonthCharges": 1.5,
    "BillingRecords": [],
    "MonthlyChargesStorage": 0.5,
    "MonthlyChargesEUTraffic": 0.2,
    "MonthlyChargesUSTraffic": 0.3,
    "MonthlyChargesASIATraffic": 0.1,
    "MonthlyChargesSATraffic": 0.05,
}

APPLY_CODE_RESPONSE = {"ErrorKey": "code.invalid"}


def _make_mock_response(json_data, status_code=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    return mock_resp


class TestStatsGet(unittest.TestCase):
    """Tests for Stats.get() — Issue C2: broken URL /statistics?dateFrom"""

    def setUp(self):
        from bunnyhop.stats import Stats
        self.stats = Stats("test-api-key")

    @patch("requests.request")
    def test_get_url_does_not_contain_literal_dateFrom(self, mock_request):
        """
        Issue C2: The URL must be /statistics — NOT /statistics?dateFrom
        (the old code hard-coded '?dateFrom' as literal text in the path).
        """
        mock_request.return_value = _make_mock_response(STATS_RESPONSE)
        self.stats.get()

        call_kwargs = mock_request.call_args
        url = call_kwargs[1].get("url") or call_kwargs[0][1]
        # The URL path must end with /statistics, not /statistics?dateFrom
        self.assertTrue(
            url.endswith("/statistics"),
            msg=f"Expected URL to end with '/statistics', got: {url!r}",
        )
        self.assertNotIn(
            "?dateFrom",
            url,
            msg=f"URL must not contain literal '?dateFrom' in the path, got: {url!r}",
        )

    @patch("requests.request")
    def test_get_passes_date_params_via_params_kwarg(self, mock_request):
        """
        Date filters must be passed via the params dict, not embedded in the URL.
        """
        mock_request.return_value = _make_mock_response(STATS_RESPONSE)
        self.stats.get(date_from="2024-01-01", date_to="2024-12-31")

        call_kwargs = mock_request.call_args
        params = call_kwargs[1].get("params") or {}
        self.assertIn(
            "dateFrom",
            params,
            msg="'dateFrom' must be passed as a query param, not baked into the URL",
        )
        self.assertEqual(params["dateFrom"], "2024-01-01")
        self.assertIn("dateTo", params)
        self.assertEqual(params["dateTo"], "2024-12-31")

    @patch("requests.request")
    def test_get_returns_stats_instance(self, mock_request):
        """Stats.get() must return a Stats instance."""
        from bunnyhop.stats import Stats
        mock_request.return_value = _make_mock_response(STATS_RESPONSE)
        result = self.stats.get()
        self.assertIsInstance(result, Stats)

    @patch("requests.request")
    def test_get_uses_get_method(self, mock_request):
        """Stats.get() must use the HTTP GET method."""
        mock_request.return_value = _make_mock_response(STATS_RESPONSE)
        self.stats.get()
        call_kwargs = mock_request.call_args
        method = call_kwargs[1].get("method") or call_kwargs[0][0]
        self.assertEqual(method, "GET")


class TestBillingApplyCode(unittest.TestCase):
    """Tests for Billing.apply_code() — Issue M8: URL injection"""

    def setUp(self):
        from bunnyhop.billing import Billing
        self.billing = Billing("test-api-key")

    @patch("requests.request")
    def test_apply_code_coupon_not_embedded_in_url(self, mock_request):
        """
        Issue M8: couponCode must NOT be interpolated directly into the URL string.
        The URL must be /billing/applycode without any query string baked in.
        """
        mock_request.return_value = _make_mock_response(APPLY_CODE_RESPONSE)
        self.billing.apply_code("my-coupon-123")

        call_kwargs = mock_request.call_args
        url = call_kwargs[1].get("url") or call_kwargs[0][1]
        self.assertNotIn(
            "my-coupon-123",
            url,
            msg=f"coupon_code must not be embedded directly in the URL, got: {url!r}",
        )
        self.assertTrue(
            url.endswith("/billing/applycode"),
            msg=f"Expected URL to end with '/billing/applycode', got: {url!r}",
        )

    @patch("requests.request")
    def test_apply_code_coupon_passed_as_param(self, mock_request):
        """
        Issue M8: couponCode must be passed via the params dict so requests
        can URL-encode it safely.
        """
        mock_request.return_value = _make_mock_response(APPLY_CODE_RESPONSE)
        self.billing.apply_code("my-coupon-123")

        call_kwargs = mock_request.call_args
        params = call_kwargs[1].get("params") or {}
        self.assertIn(
            "couponCode",
            params,
            msg="'couponCode' must be passed in the params dict",
        )
        self.assertEqual(params["couponCode"], "my-coupon-123")

    @patch("requests.request")
    def test_apply_code_special_chars_not_in_url(self, mock_request):
        """
        Issue M8: a coupon with special characters must not appear raw in the URL.
        This verifies the injection fix handles unsafe input correctly.
        """
        mock_request.return_value = _make_mock_response(APPLY_CODE_RESPONSE)
        dangerous_code = "code&inject=evil<script>"
        self.billing.apply_code(dangerous_code)

        call_kwargs = mock_request.call_args
        url = call_kwargs[1].get("url") or call_kwargs[0][1]
        self.assertNotIn(
            dangerous_code,
            url,
            msg="Unsafe coupon code must not appear verbatim in the URL",
        )

    @patch("requests.request")
    def test_apply_code_uses_get_method(self, mock_request):
        """Billing.apply_code() must use the HTTP GET method."""
        mock_request.return_value = _make_mock_response(APPLY_CODE_RESPONSE)
        self.billing.apply_code("some-code")
        call_kwargs = mock_request.call_args
        method = call_kwargs[1].get("method") or call_kwargs[0][0]
        self.assertEqual(method, "GET")


class TestBillingGet(unittest.TestCase):
    """Tests for Billing.get()"""

    def setUp(self):
        from bunnyhop.billing import Billing
        self.billing = Billing("test-api-key")

    @patch("requests.request")
    @patch("bunnyhop.billing.BillingSummary")
    def test_get_returns_billing_summary_instance(self, mock_summary_cls, mock_request):
        """Billing.get() must return a BillingSummary instance."""
        mock_request.return_value = _make_mock_response(BILLING_SUMMARY_RESPONSE)
        mock_instance = MagicMock()
        mock_summary_cls.return_value = mock_instance
        result = self.billing.get()
        # Verify BillingSummary was called (i.e., get() constructs and returns one)
        mock_summary_cls.assert_called_once()
        self.assertIs(result, mock_instance)

    @patch("requests.request")
    @patch("bunnyhop.billing.BillingSummary")
    def test_get_calls_billing_endpoint(self, mock_summary_cls, mock_request):
        """Billing.get() must call the /billing endpoint."""
        mock_request.return_value = _make_mock_response(BILLING_SUMMARY_RESPONSE)
        mock_summary_cls.return_value = MagicMock()
        self.billing.get()
        call_kwargs = mock_request.call_args
        url = call_kwargs[1].get("url") or call_kwargs[0][1]
        self.assertTrue(
            url.endswith("/billing"),
            msg=f"Expected URL to end with '/billing', got: {url!r}",
        )


if __name__ == "__main__":
    unittest.main()
