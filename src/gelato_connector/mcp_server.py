"""Antigravity MCP JSON-RPC 2.0 Server for Gelato Connector.

Engineered by 1nc0gn30 (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

from . import __version__
from .artwork_auditor import audit_artwork
from .catalog import GELATO_PRODUCTS, get_product, search_catalog
from .client import GelatoClient
from .margin_engine import calculate_margins
from .shipping_engine import get_shipping_quote

TOOLS: List[Dict[str, Any]] = [
    {
        "name": "gelato_search_catalog",
        "description": "Search Gelato localized catalog (acrylic glass, brushed aluminum, framed canvas, organic tees, mugs, journals) by query or category.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query or keyword (e.g. 'acrylic', 'aluminum', 'canvas', 'organic')"},
                "category": {"type": "string", "description": "Category filter (e.g. 'Wall Art', 'Apparel', 'Home & Living')"}
            }
        }
    },
    {
        "name": "gelato_get_shipping_quote",
        "description": "Calculate localized shipping rates, transit times, and duty savings across the 10 bundled hub countries (US, UK, DE, FR, IT, CA, AU, etc.).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "Gelato product ID or slug (e.g. 'acrylic_print_16x24', 'stanley_stella_organic_tee')"},
                "destination_country": {"type": "string", "description": "Two-letter country code ('US', 'DE', 'UK', 'FR', 'CA', 'AU')", "default": "US"},
                "is_express": {"type": "boolean", "description": "Request express courier shipping", "default": False},
                "quantity": {"type": "integer", "description": "Order quantity", "default": 1}
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "gelato_calculate_margins",
        "description": "Calculate production costs, shipping, platform fees (Etsy/Shopify), net margins, and break-even prices in USD, EUR, or GBP.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "Gelato product ID or slug"},
                "retail_price": {"type": "number", "description": "Intended retail price"},
                "currency": {"type": "string", "description": "Currency code ('USD', 'EUR', 'GBP')", "default": "USD"},
                "channel": {"type": "string", "description": "Sales channel ('etsy', 'shopify', 'direct')", "default": "etsy"},
                "destination_country": {"type": "string", "description": "Country code for localized production", "default": "US"},
                "quantity": {"type": "integer", "description": "Order quantity", "default": 1}
            },
            "required": ["product_id", "retail_price"]
        }
    },
    {
        "name": "gelato_audit_print_spec",
        "description": "Audit artwork pixel resolution, aspect ratio, and bleed compliance against Gelato manufacturing specs to ensure 300+ DPI.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "Gelato product ID or slug"},
                "image_width_px": {"type": "integer", "description": "Image width in pixels"},
                "image_height_px": {"type": "integer", "description": "Image height in pixels"}
            },
            "required": ["product_id", "image_width_px", "image_height_px"]
        }
    },
    {
        "name": "gelato_create_order_payload",
        "description": "Generate schema-valid Gelato API v2 order creation payload ready for publishing or API dispatch.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "Gelato product ID or slug"},
                "image_url": {"type": "string", "description": "Public HTTPS artwork URL"},
                "recipient_name": {"type": "string", "description": "Customer name", "default": "Jane Doe"},
                "address_line": {"type": "string", "description": "Street address", "default": "Example Street 1"},
                "city": {"type": "string", "description": "City", "default": "Berlin"},
                "country": {"type": "string", "description": "Country code", "default": "DE"},
                "postal_code": {"type": "string", "description": "Postal code", "default": "10115"}
            },
            "required": ["product_id", "image_url"]
        }
    },
    {
        "name": "gelato_get_shop_info",
        "description": "Retrieve Gelato API connection status, plan tier, and active localized manufacturing hubs.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute tool call and return response."""
    client = GelatoClient()

    if name == "gelato_search_catalog":
        query = arguments.get("query")
        category = arguments.get("category")
        return {"products": search_catalog(query, category)}

    elif name == "gelato_get_shipping_quote":
        return get_shipping_quote(
            product_id=arguments["product_id"],
            destination_country=arguments.get("destination_country", "US"),
            is_express=arguments.get("is_express", False),
            quantity=int(arguments.get("quantity", 1))
        )

    elif name == "gelato_calculate_margins":
        return calculate_margins(
            product_id=arguments["product_id"],
            retail_price=float(arguments["retail_price"]),
            currency=arguments.get("currency", "USD"),
            channel=arguments.get("channel", "etsy"),
            destination_country=arguments.get("destination_country", "US"),
            quantity=int(arguments.get("quantity", 1))
        )

    elif name == "gelato_audit_print_spec":
        return audit_artwork(
            product_id=arguments["product_id"],
            image_width_px=int(arguments["image_width_px"]),
            image_height_px=int(arguments["image_height_px"])
        )

    elif name == "gelato_create_order_payload":
        return client.create_order_payload(
            product_id=arguments["product_id"],
            image_url=arguments["image_url"],
            recipient_name=arguments.get("recipient_name", "Jane Doe"),
            address_line=arguments.get("address_line", "Example Street 1"),
            city=arguments.get("city", "Berlin"),
            country=arguments.get("country", "DE"),
            postal_code=arguments.get("postal_code", "10115")
        )

    elif name == "gelato_get_shop_info":
        return client.get_shop_info()

    raise ValueError(f"Unknown tool: {name}")


def handle_request(req: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Dispatch one JSON-RPC 2.0 message. Returns None for notifications."""
    req_id = req.get("id")
    method = req.get("method")
    if req_id is None and isinstance(method, str) and method.startswith("notifications/"):
        return None
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": (req.get("params") or {}).get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "gelato-connector", "version": __version__},
        }}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = req.get("params") or {}
        try:
            result = handle_tool_call(params.get("name"), params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": req_id, "result": {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}]}}
        except Exception as exc:  # tool-level failure is reported to the model, not as a protocol error
            return {"jsonrpc": "2.0", "id": req_id, "result": {
                "isError": True, "content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {method} not found"}}


def run_mcp_server() -> None:
    """Run MCP JSON-RPC 2.0 stdio server loop."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            resp = handle_request(json.loads(line))
        except json.JSONDecodeError as e:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {e}"}}
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
