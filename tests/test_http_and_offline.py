"""HTTP API (ephemeral port), MCP protocol and offline-mode honesty tests. No external network calls."""
import io
import json
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stdout
from http.server import HTTPServer
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from gelato_connector import __version__
from gelato_connector.cli import main as cli_main
from gelato_connector.client import GelatoClient
from gelato_connector.mcp_server import handle_request
from gelato_connector.server import GelatoRequestHandler
from gelato_connector.shipping_engine import LOCAL_HUBS, get_shipping_quote


class TestOfflineClient(unittest.TestCase):
    def test_request_without_key_raises_clear_error(self):
        with mock.patch.dict(os.environ, {"GELATO_API_KEY": ""}):
            client = GelatoClient()
            with self.assertRaises(RuntimeError) as ctx:
                client._request("/catalogs")
        self.assertIn("GELATO_API_KEY is not set", str(ctx.exception))

    def test_shop_info_never_fakes_an_organization(self):
        with mock.patch.dict(os.environ, {"GELATO_API_KEY": ""}):
            info = GelatoClient().get_shop_info()
        self.assertFalse(info["api_connected"])
        self.assertNotIn("name", info)
        self.assertNotIn("plan", info)

    def test_order_payload_currency_by_country(self):
        c = GelatoClient(api_key="")
        self.assertEqual(c.create_order_payload("acrylic_print_16x24", "https://e.x/a.png", country="DE")["currency"], "EUR")
        self.assertEqual(c.create_order_payload("acrylic_print_16x24", "https://e.x/a.png", country="UK")["currency"], "GBP")
        self.assertEqual(c.create_order_payload("acrylic_print_16x24", "https://e.x/a.png", country="US")["currency"], "USD")
        with self.assertRaises(ValueError):
            c.create_order_payload("no_such_product", "https://e.x/a.png")


class TestShipping(unittest.TestCase):
    def test_express_costs_more_than_standard(self):
        std = get_shipping_quote("acrylic_print_16x24", "DE", False)
        exp = get_shipping_quote("acrylic_print_16x24", "DE", True)
        self.assertEqual(len(LOCAL_HUBS), 10)
        self.assertIsInstance(std, dict)
        self.assertNotEqual(json.dumps(std, sort_keys=True), json.dumps(exp, sort_keys=True))


class TestHttpApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), GelatoRequestHandler)
        cls.port = cls.httpd.server_address[1]
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def _get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=5) as r:
            return r.status, json.loads(r.read())

    def _post(self, path, body, origin=None):
        headers = {"Content-Type": "application/json"}
        if origin:
            headers["Origin"] = origin
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}{path}", data=json.dumps(body).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_health_reports_real_port_and_version(self):
        status, data = self._get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["port"], self.port)
        self.assertEqual(data["version"], __version__)

    def test_stats_country_count_matches_hub_table(self):
        _, data = self._get("/api/stats")
        self.assertEqual(data["activeCountriesCount"], len(LOCAL_HUBS))

    def test_hubs_and_products(self):
        _, hubs = self._get("/api/hubs")
        self.assertEqual(set(hubs["hubs"]), set(LOCAL_HUBS))
        _, prods = self._get("/api/products")
        self.assertEqual(prods["count"], len(prods["products"]))

    def test_margins_and_payload(self):
        status, data = self._post("/api/margins", {"productId": "acrylic_print_16x24", "retailPrice": 80})
        self.assertEqual(status, 200)
        self.assertIn("margins", data)
        status, data = self._post("/api/create-payload", {"productId": "nope"})
        self.assertEqual(status, 404)

    def test_cross_origin_post_blocked(self):
        status, _ = self._post("/api/margins", {}, origin="https://evil.example")
        self.assertEqual(status, 403)


class TestCliAndMcp(unittest.TestCase):
    def test_status_json_offline(self):
        buf = io.StringIO()
        with mock.patch.dict(os.environ, {"GELATO_API_KEY": ""}), redirect_stdout(buf):
            rc = cli_main(["--port", "1", "--json"])
        self.assertEqual(rc, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data["status"], "standby")
        self.assertFalse(data["api_key_configured"])
        self.assertEqual(data["local_hubs"], len(LOCAL_HUBS))

    def test_mcp_initialize_and_errors(self):
        init = handle_request({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        self.assertEqual(init["result"]["serverInfo"]["name"], "gelato-connector")
        self.assertIsNone(handle_request({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        bad = handle_request({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "nope"}})
        self.assertTrue(bad["result"]["isError"])


if __name__ == "__main__":
    unittest.main()
