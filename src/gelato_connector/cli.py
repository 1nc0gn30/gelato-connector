"""Command Line Interface for Gelato Connector.

Engineered by 1nc0gn30 (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from typing import List, Optional

from .artwork_auditor import audit_artwork_dimensions
from .catalog import list_products
from .margin_engine import calculate_multi_channel_margins
from .mcp_server import run_mcp_server
from .server import run_server
from .shipping_engine import get_shipping_quote


def _default_bind_host() -> str:
    """Bind address: localhost unless explicitly opted in via $ZOTH_BIND_HOST or
    $HOST (IP literal only; zsh sets HOST to the hostname) or --host."""
    import ipaddress
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


# ANSI Formatting
C_GOLD = "\033[38;5;214m"
C_CYAN = "\033[38;5;51m"
C_GREEN = "\033[38;5;48m"
C_RED = "\033[38;5;196m"
C_AMBER = "\033[38;5;208m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"


def print_banner() -> None:
    print(f"{C_GOLD}{C_BOLD}🌍 GELATO CONNECTOR v2.5.0{C_RESET}")
    print(f"{C_DIM}Gelato Open API v2 Connector & Localized 32-Country Routing Optimizer{C_RESET}")
    print(f"{C_DIM}Engineered by 1nc0gn30 (@1nc0gn30) • NullAI Platform{C_RESET}\n")


def cmd_status(host: str = "127.0.0.1", port: int = 8116, as_json: bool = False) -> int:
    url = f"http://{host}:{port}/health"
    live_info = None
    try:
        with urllib.request.urlopen(url, timeout=2.0) as resp:
            live_info = json.loads(resp.read().decode("utf-8"))
    except Exception:
        pass

    products = list_products()

    data = {
        "status": "online" if live_info else "standby",
        "service": "gelato-connector",
        "version": "2.5.0",
        "port": port,
        "products_count": len(products),
        "supported_countries": 32,
        "license": "100% Free & Open Access (Zero Paywalls)",
        "daemon": live_info,
    }

    if as_json:
        print(json.dumps(data, indent=2))
        return 0

    print_banner()
    state_color = C_GREEN if live_info else C_AMBER
    print(f"Daemon Status:      {state_color}{data['status'].upper()}{C_RESET} ({url})")
    print(f"Catalog Products:   {C_CYAN}{data['products_count']} items cataloged{C_RESET}")
    print(f"Localized Hubs:     {C_GOLD}32 active sovereign countries{C_RESET}")
    print(f"Access Guarantee:   100% Free & Open Access (Zero Paywalls)")
    print()
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gelato-connector",
        description="Gelato Open API v2 Connector, Localized Multi-Country POD Router, & Antigravity MCP Suite"
    )
    parser.add_argument("-v", "--version", action="version", version="gelato-connector 2.5.0")
    parser.add_argument("--status", action="store_true", help="Print local service status and configuration")
    parser.add_argument("--json", action="store_true", help="Output status/telemetry as JSON")
    parser.add_argument("--host", default=_default_bind_host(), help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8116, help="Port to bind/check (default: 8116)")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: status
    status_p = subparsers.add_parser("status", help="Check local service and API configuration status")
    status_p.add_argument("--host", default="127.0.0.1", help="Host interface")
    status_p.add_argument("--port", type=int, default=8116, help="Port (default: 8116)")
    status_p.add_argument("--json", action="store_true", help="Output status report as JSON")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Run the HTTP & REST API daemon")
    serve_parser.add_argument("--port", type=int, default=8116, help="HTTP listening port (default: 8116)")
    serve_parser.add_argument("--host", type=str, default=_default_bind_host(), help="Host interface")

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

    args = parser.parse_args(argv)

    if getattr(args, "status", False) or (getattr(args, "json", False) and not args.command):
        return cmd_status(host=args.host, port=args.port, as_json=True if getattr(args, "json", False) else False)

    cmd = args.command or "serve"

    if cmd == "status":
        return cmd_status(host=args.host, port=args.port, as_json=args.json)
    elif cmd == "serve":
        run_server(port=args.port, host=args.host)
        return 0
    elif cmd == "mcp":
        run_mcp_server()
        return 0
    elif cmd == "catalog":
        items = list_products(args.category)
        print(json.dumps(items, indent=2))
        return 0
    elif cmd == "shipping":
        quote = get_shipping_quote(
            product_id=args.product,
            destination_country=args.country,
            is_express=args.express
        )
        print(json.dumps(quote, indent=2))
        return 0
    elif cmd == "margins":
        res = calculate_multi_channel_margins(
            product_id=args.product,
            retail_price=args.price,
            currency=args.currency,
            destination_country=args.country
        )
        print(json.dumps(res, indent=2))
        return 0
    elif cmd == "audit":
        audit = audit_artwork_dimensions(
            product_id=args.product,
            width_px=args.width,
            height_px=args.height,
            file_name=args.name
        )
        print(json.dumps(audit, indent=2))
        return 0
    elif cmd == "info":
        return cmd_status(host=args.host, port=args.port, as_json=False)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
