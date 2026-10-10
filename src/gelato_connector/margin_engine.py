"""Gelato Multi-Currency Margin & Profit Calculator Engine.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from .catalog import get_product
from .shipping_engine import get_shipping_quote


def calculate_margins(
    product_id: Any,
    retail_price: float,
    currency: str = "USD",
    channel: str = "etsy",
    destination_country: str = "US",
    quantity: int = 1
) -> Dict[str, Any]:
    """Calculate exact costs, platform fees, net profit, and margins across currencies."""
    product = get_product(product_id)
    if not product:
        raise ValueError(f"Unknown product ID '{product_id}'")

    curr = currency.upper()
    if curr == "EUR":
        base_cost = product["base_cost_eur"]
    elif curr == "GBP":
        base_cost = product["base_cost_gbp"]
    else:
        base_cost = product["base_cost_usd"]

    # Production cost
    total_production = round(base_cost * quantity, 2)

    # Shipping cost
    ship_data = get_shipping_quote(product["id"], destination_country, is_express=False, quantity=quantity)
    shipping_cost = ship_data["shipping_cost"]

    # Cost of Goods Sold (COGS)
    total_cogs = round(total_production + shipping_cost, 2)

    # Platform Fees
    total_revenue = round(retail_price * quantity, 2)
    ch = channel.lower()

    if ch == "etsy":
        # Etsy: 6.5% transaction + 3% + 0.25 payment + 0.20 listing
        txn = total_revenue * 0.065
        proc = (total_revenue * 0.03) + 0.25
        listing = 0.20
        total_fees = round(txn + proc + listing, 2)
    elif ch == "shopify":
        # Shopify: 2.9% + 0.30
        total_fees = round((total_revenue * 0.029) + 0.30, 2)
    else:
        # Direct / Web3 / Solana: ~0.30 fixed gas/rail
        total_fees = round((total_revenue * 0.029) + 0.30, 2)

    total_expenses = round(total_cogs + total_fees, 2)
    net_profit = round(total_revenue - total_expenses, 2)
    margin_pct = round((net_profit / total_revenue) * 100, 1) if total_revenue > 0 else 0.0

    # Break-even price
    if ch == "etsy":
        break_even_total = (total_cogs + 0.45) / 0.905
    else:
        break_even_total = (total_cogs + 0.30) / 0.971
    break_even_unit = round(break_even_total / quantity, 2)

    # Recommended Pricing Tiers
    rec_30 = round(break_even_unit / 0.70, 2)
    rec_50 = round(break_even_unit / 0.50, 2)
    rec_65 = round(break_even_unit / 0.35, 2)

    return {
        "product_id": product["id"],
        "product_title": product["title"],
        "category": product["category"],
        "currency": curr,
        "channel": channel.upper(),
        "destination_country": destination_country.upper(),
        "quantity": quantity,
        "retail_price_unit": retail_price,
        "total_revenue": total_revenue,
        "base_production_cost": total_production,
        "shipping_cost": shipping_cost,
        "is_local_production": ship_data["is_local_production"],
        "total_cogs": total_cogs,
        "platform_fees": total_fees,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "profit_margin_pct": margin_pct,
        "break_even_price": break_even_unit,
        "freight_savings": ship_data.get("freight_savings_vs_cross_border", 0.0),
        "recommended_pricing": {
            "tier_30_pct": rec_30,
            "tier_50_pct": rec_50,
            "tier_65_pct": rec_65
        }
    }


def calculate_multi_channel_margins(
    product_id: Any,
    retail_price: float,
    currency: str = "USD",
    destination_country: str = "US"
) -> Dict[str, Any]:
    """Compare Etsy, Shopify, and Direct channels for a Gelato product."""
    product = get_product(product_id)
    if not product:
        raise ValueError(f"Unknown product ID '{product_id}'")

    channels = ["etsy", "shopify", "direct"]
    results = {}

    for ch in channels:
        results[ch] = calculate_margins(
            product_id=product["id"],
            retail_price=retail_price,
            currency=currency,
            channel=ch,
            destination_country=destination_country
        )

    return {
        "product": {
            "id": product["id"],
            "title": product["title"],
            "category": product["category"],
            "base_cost_usd": product["base_cost_usd"],
            "base_cost_eur": product["base_cost_eur"],
            "base_cost_gbp": product["base_cost_gbp"]
        },
        "retail_price": retail_price,
        "currency": currency.upper(),
        "destination_country": destination_country.upper(),
        "channels": results
    }
