"""Gelato API v2 Client.

Engineered by 1nc0gn30 (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional
from .catalog import GELATO_PRODUCTS, get_product


class GelatoClient:
    """Gelato REST API v2 Client with Live & Offline Deterministic Modes."""

    # Gelato Product API (catalog listing). Used live only when GELATO_API_KEY is set.
    BASE_URL = "https://product.gelatoapis.com/v3"

    OFFLINE_MESSAGE = (
        "GELATO_API_KEY is not set. Live Gelato API calls are disabled; catalog, shipping, "
        "margin, audit and order-payload tools use the bundled offline reference data. "
        "Create a key in the Gelato dashboard (Developer > API Keys) and export GELATO_API_KEY to enable live mode."
    )

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("GELATO_API_KEY", "")
        self.is_live = bool(self.api_key)

    def _request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an authenticated HTTP request. Raises when no API key is configured."""
        if not self.is_live:
            raise RuntimeError(self.OFFLINE_MESSAGE)

        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "gelato-connector/2.5.0"
        }

        body = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Gelato API Error {e.code}: {err_body}")
        except Exception as e:
            raise RuntimeError(f"Gelato Connection Error: {e}")

    def get_shop_info(self) -> Dict[str, Any]:
        """Report API connection status. Live mode verifies the key against GET /v3/catalogs."""
        if not self.is_live:
            return {"api_connected": False, "mode": "OFFLINE", "error": self.OFFLINE_MESSAGE}
        catalogs = self._request("/catalogs")
        items = catalogs.get("data", catalogs) if isinstance(catalogs, dict) else catalogs
        return {"api_connected": True, "mode": "LIVE", "catalogs_count": len(items) if isinstance(items, list) else None}

    def get_catalog(self) -> List[Dict[str, Any]]:
        """List localized Gelato products."""
        if not self.is_live:
            return GELATO_PRODUCTS
        return self._request("/catalogs")

    def create_order_payload(
        self,
        product_id: Any,
        image_url: str,
        recipient_name: str = "Jane Doe",
        address_line: str = "Example Street 1",
        city: str = "Berlin",
        country: str = "DE",
        postal_code: str = "10115",
        order_reference: str = "ORDER-SOV-001"
    ) -> Dict[str, Any]:
        """Build schema-valid Gelato API v2 order creation payload."""
        product = get_product(product_id)
        if not product:
            raise ValueError(f"Unknown product ID '{product_id}'")

        payload = {
            "orderType": "order",
            "orderReferenceId": order_reference,
            "customerReferenceId": f"CUST-{order_reference}",
            "currency": "EUR" if country in ["DE", "FR", "IT", "ES", "NL"] else ("GBP" if country == "UK" else "USD"),
            "shippingAddress": {
                "firstName": recipient_name.split()[0] if " " in recipient_name else recipient_name,
                "lastName": recipient_name.split()[-1] if " " in recipient_name else "Recipient",
                "addressLine1": address_line,
                "city": city,
                "country": country,
                "postCode": postal_code,
                "email": "customer@example.com"
            },
            "items": [
                {
                    "itemReferenceId": f"ITEM-{product['id']}-01",
                    "productUid": f"gelato_{product['id']}",
                    "files": [
                        {
                            "type": "default",
                            "url": image_url
                        }
                    ],
                    "quantity": 1
                }
            ]
        }
        return payload
