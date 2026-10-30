#!/usr/bin/env python3
"""Root launcher for Gelato Connector server.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add src to sys.path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gelato_connector.server import run_server


def main():
    parser = argparse.ArgumentParser(description="Gelato Connector Standalone Workstation Server")
    parser.add_argument("--port", type=int, default=8116, help="Port to bind (default: 8116)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    args = parser.parse_args()
    run_server(port=args.port, host=args.host)


if __name__ == "__main__":
    main()
