"""Gelato Product Catalog & Localized Production Database.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

GELATO_PRODUCTS: List[Dict[str, Any]] = [
    {
        "id": "acrylic_print_16x24",
        "title": "Acrylic Glass Print (16x24 in / 40x60 cm)",
        "category": "Wall Art / Acrylic",
        "description": "High-end 4mm crystal clear acrylic glass with polished edges. Ultra-vivid colors and depth effect. Popular for modern gallery art.",
        "base_cost_usd": 29.50,
        "base_cost_eur": 27.20,
        "base_cost_gbp": 23.40,
        "print_width_px": 4800,
        "print_height_px": 7200,
        "recommended_dpi": 300,
        "bleed_mm": 3.0,
        "local_production_countries": ["US", "DE", "UK", "CA", "AU", "FR", "NL"],
        "popular": True,
        "tags": ["wall-art", "acrylic", "modern", "high-ticket", "gallery"]
    },
    {
        "id": "aluminum_print_16x24",
        "title": "Brushed Aluminum Dibond Print (16x24 in / 40x60 cm)",
        "category": "Wall Art / Aluminum",
        "description": "Matte, glare-free metallic direct print on 3mm composite aluminum. Extremely durable, lightweight, water-resistant.",
        "base_cost_usd": 26.80,
        "base_cost_eur": 24.90,
        "base_cost_gbp": 21.20,
        "print_width_px": 4800,
        "print_height_px": 7200,
        "recommended_dpi": 300,
        "bleed_mm": 3.0,
        "local_production_countries": ["US", "DE", "UK", "CA", "AU", "NO"],
        "popular": True,
        "tags": ["wall-art", "aluminum", "metallic", "industrial", "premium"]
    },
    {
        "id": "wooden_framed_canvas_16x24",
        "title": "Framed Wooden Canvas Wrap (16x24 in)",
        "category": "Wall Art / Canvas",
        "description": "FSC-certified pine frame with archival grade canvas. Floating shadow-box wood frame in natural oak, black, or white.",
        "base_cost_usd": 24.20,
        "base_cost_eur": 22.50,
        "base_cost_gbp": 19.30,
        "print_width_px": 5100,
        "print_height_px": 7500,
        "recommended_dpi": 300,
        "bleed_mm": 5.0,
        "local_production_countries": ["US", "UK", "DE", "FR", "ES", "IT", "CA", "AU", "JP"],
        "popular": True,
        "tags": ["wall-art", "framed-canvas", "cottagecore", "wood-frame", "bestseller"]
    },
    {
        "id": "stanley_stella_organic_tee",
        "title": "Stanley/Stella Organic Creator Unisex T-Shirt",
        "category": "Apparel / Organic T-Shirts",
        "description": "100% GOTS certified organic ring-spun combed cotton (180 GSM). The benchmark for eco-conscious luxury street fashion in the EU & UK.",
        "base_cost_usd": 12.40,
        "base_cost_eur": 10.90,
        "base_cost_gbp": 9.50,
        "print_width_px": 4000,
        "print_height_px": 4800,
        "recommended_dpi": 300,
        "bleed_mm": 0.0,
        "local_production_countries": ["DE", "UK", "FR", "NL", "ES", "IT", "US"],
        "popular": True,
        "tags": ["apparel", "organic", "eco-friendly", "gots-cotton", "stanley-stella", "bestseller"]
    },
    {
        "id": "ceramic_mug_15oz",
        "title": "Large Ceramic Accent Mug 15oz",
        "category": "Home & Living / Mugs",
        "description": "Heavyweight 15oz ceramic mug with colored interior and matching handle. Microwave and dishwasher safe with high-durability sublimation glaze.",
        "base_cost_usd": 5.95,
        "base_cost_eur": 5.40,
        "base_cost_gbp": 4.60,
        "print_width_px": 2850,
        "print_height_px": 1200,
        "recommended_dpi": 300,
        "bleed_mm": 2.0,
        "local_production_countries": ["US", "UK", "DE", "CA", "AU"],
        "popular": True,
        "tags": ["home-and-living", "mugs", "ceramic", "coffee", "bestseller", "cottagecore"]
    },
    {
        "id": "enamel_campfire_mug",
        "title": "Vintage Stainless Steel Enamel Campfire Mug 12oz",
        "category": "Home & Living / Outdoor",
        "description": "Retro enamel coated camp mug with silver rim. Lightweight, durable, rust-resistant. Perfect for camping, hiking, and cabin decor.",
        "base_cost_usd": 7.40,
        "base_cost_eur": 6.80,
        "base_cost_gbp": 5.80,
        "print_width_px": 2500,
        "print_height_px": 950,
        "recommended_dpi": 300,
        "bleed_mm": 2.0,
        "local_production_countries": ["US", "DE", "UK", "PL"],
        "popular": False,
        "tags": ["outdoor", "camp-mug", "enamel", "vintage", "rustic"]
    },
    {
        "id": "hardcover_photo_journal",
        "title": "Hardcover Matte Photo Journal (A5 / 128 Pages)",
        "category": "Stationery / Journals",
        "description": "Full wraparound matte hardcover with 90 GSM unlined or ruled archival paper. 128 pages with case-bound spine and ribbon marker.",
        "base_cost_usd": 8.90,
        "base_cost_eur": 8.10,
        "base_cost_gbp": 6.90,
        "print_width_px": 3700,
        "print_height_px": 2600,
        "recommended_dpi": 300,
        "bleed_mm": 4.0,
        "local_production_countries": ["US", "DE", "UK", "NL", "AU"],
        "popular": False,
        "tags": ["stationery", "journal", "hardcover", "notebook", "gift"]
    }
]

# Aliases and Slugs
PRODUCTS = GELATO_PRODUCTS

SLUG_MAP: Dict[str, str] = {
    "acrylic_print": "acrylic_print_16x24",
    "acrylic": "acrylic_print_16x24",
    "aluminum_print": "aluminum_print_16x24",
    "aluminum": "aluminum_print_16x24",
    "dibond": "aluminum_print_16x24",
    "framed_canvas": "wooden_framed_canvas_16x24",
    "canvas": "wooden_framed_canvas_16x24",
    "organic_tee": "stanley_stella_organic_tee",
    "stanley_stella": "stanley_stella_organic_tee",
    "mug_15oz": "ceramic_mug_15oz",
    "mug": "ceramic_mug_15oz",
    "camp_mug": "enamel_campfire_mug",
    "enamel_mug": "enamel_campfire_mug",
    "journal": "hardcover_photo_journal",
    "notebook": "hardcover_photo_journal"
}


def search_catalog(query: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Filter catalog products by search keyword or category."""
    results = GELATO_PRODUCTS
    if query:
        q = query.lower()
        results = [
            p for p in results
            if q in p["title"].lower()
            or q in p["id"].lower()
            or any(q in t for t in p["tags"])
        ]
    if category:
        c = category.lower()
        results = [p for p in results if c in p["category"].lower()]
    return results


def list_products(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all Gelato products, optionally filtered by category."""
    return search_catalog(category=category)


def get_product(identifier: Any) -> Optional[Dict[str, Any]]:
    """Retrieve product by exact ID, slug, or title match."""
    if not identifier:
        return None
    val_str = str(identifier).strip().lower().replace(" ", "_").replace("-", "_")

    # Direct ID match
    for p in GELATO_PRODUCTS:
        if p["id"] == val_str:
            return p

    # Slug map lookup
    if val_str in SLUG_MAP:
        target_id = SLUG_MAP[val_str]
        for p in GELATO_PRODUCTS:
            if p["id"] == target_id:
                return p

    # Substring search
    for p in GELATO_PRODUCTS:
        if val_str in p["id"] or val_str in p["title"].lower().replace(" ", "_"):
            return p
    return None
