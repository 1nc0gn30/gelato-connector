"""Gelato API v2 Client.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
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

    BASE_URL = "https://order.gelatoapis.com/v2"

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("GELATO_API_KEY", "")
        self.is_live = bool(self.api_key)

    def _request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an authenticated HTTP request or fallback to mock mode."""
        if not self.is_live:
            return self._mock_response(endpoint, method, data)

        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "GelatoConnector-Antigravity/1.0.0"
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
        """Retrieve connected Gelato store status and production routing capabilities."""
        if not self.is_live:
            return {
                "organization_id": "org_nullai_1nc0gn30",
                "name": "Neal Frazier Tech Sovereign Print Hub",
                "plan": "Gelato Connect Sovereign Enterprise",
                "mode": "OFFLINE_DETERMINISTIC",
                "active_hubs_count": 32,
                "supported_currencies": ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"],
                "api_connected": False,
                "status": "Ready for Autonomous Dispatch"
            }
        return self._request("/organizations/me")

    def get_catalog(self) -> List[Dict[str, Any]]:
        """List localized Gelato products."""
        if not self.is_live:
            return GELATO_PRODUCTS
        return self._request("/catalog/products")

    def create_order_payload(
        self,
        product_id: Any,
        image_url: str,
        recipient_name: str = "Jane Doe",
        address_line: str = "123 Sovereign Way",
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

    def _mock_response(self, endpoint: str, method: str, data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Internal mock handler for testing without API keys."""
        if "catalog" in endpoint:
            return {"products": GELATO_PRODUCTS}
        if "orders" in endpoint:
            return {
                "id": "mock_gelato_order_99823",
                "status": "created",
                "productionCountry": "DE",
                "mode": "MOCK_MODE"
            }
        return {"status": "ok", "mode": "MOCK_MODE", "endpoint": endpoint}
