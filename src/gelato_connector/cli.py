"""CLI Entrypoint for Gelato Connector.

Supports server daemon, Model Context Protocol (MCP), and local utility commands.
"""

import argparse
import json
import sys

from .artwork_auditor import audit_artwork_dimensions
from .catalog import list_products
from .margin_engine import calculate_multi_channel_margins
from .mcp_server import run_mcp_server
from .server import run_server
from .shipping_engine import get_shipping_quote


def _default_bind_host() -> str:
    """Bind address: localhost unless explicitly opted in via $ZOTH_BIND_HOST or
    $HOST (IP literal only; zsh sets HOST to the hostname) or --host."""
    import ipaddress, os
    for var in ("ZOTH_BIND_HOST", "HOST"):
        val = os.environ.get(var, "").strip()
        if val == "localhost":
            return "127.0.0.1"
        if val:
            try:
                ipaddress.ip_address(val)
                return val
            except ValueError:
                pass
    return "127.0.0.1"



def main():
    parser = argparse.ArgumentParser(
        prog="gelato-connector",
        description="Gelato Open API v2 Connector, Localized Multi-Country POD Router, & Antigravity MCP Suite"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Run the HTTP & REST API daemon")
    serve_parser.add_argument("--port", type=int, default=8116, help="HTTP listening port (default: 8116)")
    serve_parser.add_argument("--host", type=str, default=_default_bind_host(), help="Host interface (default: 127.0.0.1 or $ZOTH_BIND_HOST; use 0.0.0.0 only on trusted networks)")

    # Command: mcp
    subparsers.add_parser("mcp", help="Run the Antigravity Model Context Protocol (MCP) stdio server")

    # Command: catalog
    cat_parser = subparsers.add_parser("catalog", help="List localized catalog products")
    cat_parser.add_argument("--category", type=str, default=None, help="Filter by category")

    # Command: shipping
    ship_parser = subparsers.add_parser("shipping", help="Calculate localized shipping quote and transit time")
    ship_parser.add_argument("--product", type=str, default="acrylic_print_16x24", help="Product ID or slug")
    ship_parser.add_argument("--country", type=str, default="US", help="Destination country code (US, DE, UK, CA, AU)")
    ship_parser.add_argument("--express", action="store_true", help="Request express delivery")

    # Command: margins
    margin_parser = subparsers.add_parser("margins", help="Calculate multi-channel profit margins")
    margin_parser.add_argument("--product", type=str, default="acrylic_print_16x24", help="Product ID or slug")
    margin_parser.add_argument("--price", type=float, default=68.00, help="Retail sale price")
    margin_parser.add_argument("--currency", type=str, default="USD", help="Currency (USD, EUR, GBP)")
    margin_parser.add_argument("--country", type=str, default="US", help="Destination country")

    # Command: audit
    audit_parser = subparsers.add_parser("audit", help="Audit artwork dimensions against print specs")
    audit_parser.add_argument("--product", type=str, default="acrylic_print_16x24", help="Product ID or slug")
    audit_parser.add_argument("--width", type=int, required=True, help="Image width in pixels")
    audit_parser.add_argument("--height", type=int, required=True, help="Image height in pixels")
    audit_parser.add_argument("--name", type=str, default="masterpiece.png", help="Filename")

    # Command: info
    subparsers.add_parser("info", help="Show system status and API configuration")

    args = parser.parse_args()

    if args.command == "serve":
        run_server(port=args.port, host=args.host)
    elif args.command == "mcp":
        run_mcp_server()
    elif args.command == "catalog":
        items = list_products(args.category)
        print(json.dumps(items, indent=2))
    elif args.command == "shipping":
        quote = get_shipping_quote(
            product_id=args.product,
            destination_country=args.country,
            is_express=args.express
        )
        print(json.dumps(quote, indent=2))
    elif args.command == "margins":
        res = calculate_multi_channel_margins(
            product_id=args.product,
            retail_price=args.price,
            currency=args.currency,
            destination_country=args.country
        )
        print(json.dumps(res, indent=2))
    elif args.command == "audit":
        audit = audit_artwork_dimensions(
            product_id=args.product,
            width_px=args.width,
            height_px=args.height,
            file_name=args.name
        )
        print(json.dumps(audit, indent=2))
    elif args.command == "info":
        print(json.dumps({
            "service": "gelato-connector",
            "version": "1.0.0",
            "status": "ready",
            "assigned_port": 8116,
            "creator": "Neal Frazier Tech (@1nc0gn30)",
            "monetization": "Stripe ($19 lifetime) + DePay Solana Widget"
        }, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
