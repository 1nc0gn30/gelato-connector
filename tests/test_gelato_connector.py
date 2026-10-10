"""Unit tests for Gelato Connector.

100% Python Standard Library — Zero External Dependencies.
Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from gelato_connector.catalog import (
    GELATO_PRODUCTS,
    get_product,
    list_products,
    search_catalog,
)
from gelato_connector.shipping_engine import get_shipping_quote, LOCAL_HUBS
from gelato_connector.margin_engine import calculate_margins, calculate_multi_channel_margins
from gelato_connector.artwork_auditor import audit_artwork, audit_artwork_dimensions
from gelato_connector.client import GelatoClient
from gelato_connector.mcp_server import handle_tool_call, TOOLS


class TestGelatoCatalog(unittest.TestCase):
    def test_products_exist(self):
        self.assertGreaterEqual(len(GELATO_PRODUCTS), 7)

    def test_get_product_by_id_and_slug(self):
        p1 = get_product("acrylic_print_16x24")
        self.assertIsNotNone(p1)
        self.assertEqual(p1["category"], "Wall Art / Acrylic")

        p_slug = get_product("acrylic")
        self.assertIsNotNone(p_slug)
        self.assertEqual(p_slug["id"], "acrylic_print_16x24")

        p_tee = get_product("organic_tee")
        self.assertIsNotNone(p_tee)
        self.assertIn("DE", p_tee["local_production_countries"])

    def test_search_catalog(self):
        canvases = search_catalog(query="canvas")
        self.assertTrue(any(p["id"] == "wooden_framed_canvas_16x24" for p in canvases))


class TestGelatoShipping(unittest.TestCase):
    def test_domestic_us_shipping(self):
        quote = get_shipping_quote("acrylic_print_16x24", "US")
        self.assertTrue(quote["is_local_production"])
        self.assertEqual(quote["currency"], "USD")
        self.assertFalse(quote["duties_expected"])

    def test_domestic_germany_shipping(self):
        quote = get_shipping_quote("acrylic_print_16x24", "DE")
        self.assertTrue(quote["is_local_production"])
        self.assertEqual(quote["currency"], "EUR")
        self.assertGreater(quote["environmental_impact"]["carbon_reduction_pct"], 50.0)


class TestGelatoMargins(unittest.TestCase):
    def test_margins_usd(self):
        res = calculate_margins("acrylic_print_16x24", 68.00, currency="USD", channel="etsy")
        self.assertEqual(res["base_production_cost"], 29.50)
        self.assertGreater(res["net_profit"], 25.00)
        self.assertGreater(res["profit_margin_pct"], 35.0)

    def test_margins_eur(self):
        res = calculate_margins("acrylic_print_16x24", 65.00, currency="EUR", channel="shopify", destination_country="DE")
        self.assertEqual(res["currency"], "EUR")
        self.assertEqual(res["base_production_cost"], 27.20)
        self.assertGreater(res["net_profit"], 30.00)

    def test_multi_channel_margins(self):
        res = calculate_multi_channel_margins("stanley_stella_organic_tee", 34.00, currency="USD")
        self.assertIn("etsy", res["channels"])
        self.assertIn("shopify", res["channels"])
        self.assertIn("direct", res["channels"])


class TestGelatoArtworkAuditor(unittest.TestCase):
    def test_audit_high_res(self):
        res = audit_artwork_dimensions("acrylic_print_16x24", 4800, 7200)
        self.assertEqual(res["print_quality_grade"], "EXCELLENT")
        self.assertTrue(res["is_print_ready"])
        self.assertGreaterEqual(res["effective_dpi"], 300)

    def test_audit_low_res(self):
        res = audit_artwork_dimensions("acrylic_print_16x24", 1000, 1000)
        self.assertEqual(res["print_quality_grade"], "CRITICAL_LOW_RES")
        self.assertFalse(res["is_print_ready"])


class TestGelatoClientAndMCP(unittest.TestCase):
    def test_client_offline_mock(self):
        client = GelatoClient()
        info = client.get_shop_info()
        self.assertEqual(info["mode"], "OFFLINE_DETERMINISTIC")
        payload = client.create_order_payload("acrylic_print_16x24", "https://example.com/art.png")
        self.assertEqual(payload["orderType"], "order")
        self.assertIn("shippingAddress", payload)

    def test_mcp_tools(self):
        self.assertGreaterEqual(len(TOOLS), 6)
        res = handle_tool_call("gelato_search_catalog", {"query": "aluminum"})
        self.assertIn("products", res)


if __name__ == "__main__":
    unittest.main()
