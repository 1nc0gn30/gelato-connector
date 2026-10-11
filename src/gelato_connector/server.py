"""HTTP & REST API Server for Gelato Connector.

Port 8116 — Zero external runtime dependencies (100% Python Standard Library).
Provides REST endpoints and serves dark-glassmorphic frontend.
"""

import json
import os
import sys
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from .artwork_auditor import audit_artwork_dimensions
from .catalog import GELATO_PRODUCTS, get_product, list_products
from .margin_engine import calculate_margins, calculate_multi_channel_margins
from .shipping_engine import LOCAL_HUBS, get_shipping_quote


class GelatoRequestHandler(SimpleHTTPRequestHandler):
    """Handles static files from public/ and JSON API endpoints."""

    def __init__(self, *args, **kwargs):
        public_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "public"
        )
        super().__init__(*args, directory=public_dir, **kwargs)

    def _send_json(self, data, status=HTTPStatus.OK):
        """Serialize and send JSON response with standard CORS headers."""
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests for static assets and API queries."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query = parse_qs(parsed.query)

        # Health & Status
        if path in ("/health", "/api/health"):
            return self._send_json({
                "status": "healthy",
                "service": "gelato-connector",
                "version": "1.0.0",
                "port": 8116,
                "engine": "Python Standard Library (Zero External Dependencies)",
                "creator": "Neal Frazier Tech (@1nc0gn30)"
            })

        if path == "/api/stats":
            return self._send_json({
                "service": "gelato-connector",
                "status": "online",
                "port": 8116,
                "productsCount": len(GELATO_PRODUCTS),
                "hubsCount": len(LOCAL_HUBS),
                "activeCountriesCount": 32,
                "supportedCurrencies": ["USD", "EUR", "GBP", "CAD", "AUD"],
                "mcpToolsCount": 6,
                "creator": "Neal Frazier Tech (@1nc0gn30)"
            })

        # Catalog products
        if path == "/api/products":
            category = query.get("category", [None])[0]
            items = list_products(category)
            return self._send_json({
                "success": True,
                "count": len(items),
                "products": items
            })

        # Single product detail
        if path.startswith("/api/products/"):
            prod_id = path.split("/")[-1]
            p = get_product(prod_id)
            if p:
                return self._send_json({"success": True, "product": p})
            return self._send_json({"error": f"Product '{prod_id}' not found"}, status=HTTPStatus.NOT_FOUND)

        # Local hubs list
        if path == "/api/hubs":
            return self._send_json({
                "success": True,
                "hubs": LOCAL_HUBS
            })

        # Fallback to static files in public/
        return super().do_GET()

    def do_POST(self):
        """Handle POST calculation and order payload generation requests."""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 1024 * 1024:
                return self._send_json({"error": "Payload exceeds 1MB limit"}, status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            body_bytes = self.rfile.read(content_length)
            body = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except Exception as e:
            return self._send_json({"error": f"Invalid JSON body: {str(e)}"}, status=HTTPStatus.BAD_REQUEST)

        # Margin Calculation
        if path == "/api/margins":
            prod_id = body.get("productId", "acrylic_print_16x24")
            retail = float(body.get("retailPrice", 68.00))
            currency = body.get("currency", "USD")
            dest = body.get("destinationCountry", "US")

            res = calculate_multi_channel_margins(
                product_id=prod_id,
                retail_price=retail,
                currency=currency,
                destination_country=dest
            )
            return self._send_json({"success": True, "margins": res})

        # Shipping Quote
        if path == "/api/shipping":
            prod_id = body.get("productId", "acrylic_print_16x24")
            dest = body.get("destinationCountry", "US")
            is_express = bool(body.get("isExpress", False))
            quantity = int(body.get("quantity", 1))

            quote = get_shipping_quote(prod_id, dest, is_express, quantity)
            return self._send_json({"success": True, "shipping": quote})

        # Artwork Auditor
        if path == "/api/audit":
            prod_id = body.get("productId", "acrylic_print_16x24")
            w = int(body.get("widthPx", 4800))
            h = int(body.get("heightPx", 7200))
            name = body.get("fileName", "masterpiece.png")

            audit = audit_artwork_dimensions(prod_id, w, h, name)
            return self._send_json({"success": True, "audit": audit})

        # Order Payload Generator
        if path == "/api/create-payload":
            prod_id = body.get("productId", "acrylic_print_16x24")
            image_url = body.get("imageUrl", "https://example.com/artwork.png")
            name = body.get("recipientName", "Jane Doe")
            address = body.get("addressLine", "123 Sovereign Way")
            city = body.get("city", "Berlin")
            country = body.get("country", "DE")
            postal = body.get("postalCode", "10115")

            p = get_product(prod_id)
            if not p:
                return self._send_json({"error": f"Unknown product: {prod_id}"}, status=HTTPStatus.NOT_FOUND)

            order_payload = {
                "orderType": "order",
                "orderReferenceId": "ORDER-SOV-8116",
                "customerReferenceId": "CUST-SOV-8116",
                "currency": "EUR" if country in ["DE", "FR", "IT", "ES", "NL"] else ("GBP" if country == "UK" else "USD"),
                "shippingAddress": {
                    "firstName": name.split()[0] if " " in name else name,
                    "lastName": name.split()[-1] if " " in name else "Recipient",
                    "addressLine1": address,
                    "city": city,
                    "country": country,
                    "postCode": postal,
                    "email": "buyer@example.com"
                },
                "items": [
                    {
                        "itemReferenceId": f"ITEM-{p['id']}-01",
                        "productUid": f"gelato_{p['id']}",
                        "files": [{"type": "default", "url": image_url}],
                        "quantity": 1
                    }
                ]
            }
            return self._send_json({"success": True, "gelato_order_payload": order_payload})

        return self._send_json({"error": f"Path not found: {path}"}, status=HTTPStatus.NOT_FOUND)


def run_server(port=8116, host="127.0.0.1"):
    """Start the Gelato Connector HTTP daemon."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, GelatoRequestHandler)
    print(f"🌍 Gelato Connector HTTP Server active at http://{host}:{port}")
    print(f"   • Endpoints: /api/stats, /api/products, /api/hubs, /api/margins, /api/shipping, /api/audit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down Gelato Connector server gracefully...")
        httpd.server_close()
