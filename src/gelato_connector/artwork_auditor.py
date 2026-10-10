"""Gelato Artwork Specification & Bleed Auditor.

Engineered by Neal Frazier Tech (@1nc0gn30) • NullAI Platform.
100% Python Standard Library — Zero External Dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from .catalog import get_product


def audit_artwork(
    product_id: Any,
    image_width_px: int,
    image_height_px: int,
    declared_dpi: Optional[int] = None
) -> Dict[str, Any]:
    """Audit image dimensions, aspect ratio, and bleed area against Gelato print specs."""
    product = get_product(product_id)
    if not product:
        raise ValueError(f"Unknown product ID '{product_id}'")

    target_w = product["print_width_px"]
    target_h = product["print_height_px"]
    rec_dpi = product.get("recommended_dpi", 300)
    bleed_mm = product.get("bleed_mm", 0.0)

    # Compute effective DPI ratio
    width_ratio = image_width_px / target_w
    height_ratio = image_height_px / target_h
    effective_scale = min(width_ratio, height_ratio)
    effective_dpi = round(rec_dpi * effective_scale)

    status = "EXCELLENT"
    feedback = []

    if effective_dpi >= 300:
        status = "EXCELLENT"
        feedback.append("Artwork satisfies Gelato 300+ DPI museum-grade print benchmark.")
        feedback.append("Substrate color gamut and fine line fidelity fully preserved.")
    elif effective_dpi >= 200:
        status = "ACCEPTABLE"
        feedback.append(f"Effective DPI is {effective_dpi}. Meets retail printing standards, but 300 DPI recommended for acrylic/aluminum.")
    elif effective_dpi >= 150:
        status = "WARNING"
        feedback.append(f"Effective DPI is {effective_dpi}. May exhibit slight grain or softness on large wall decor.")
    else:
        status = "CRITICAL_LOW_RES"
        feedback.append(f"Effective DPI is only {effective_dpi}. Severe pixelation risk. Upscale artwork prior to publishing.")

    # Bleed Area note
    if bleed_mm > 0:
        feedback.append(f"Product requires {bleed_mm}mm perimeter bleed zone. Keep vital typography and focal points inside the inner safe area.")

    # Aspect ratio check
    target_aspect = target_w / target_h
    art_aspect = image_width_px / image_height_px
    aspect_diff = abs(target_aspect - art_aspect)

    if aspect_diff > 0.15:
        feedback.append(f"Aspect ratio discrepancy ({art_aspect:.2f} vs required {target_aspect:.2f}). Artwork may be cropped on the substrate edges.")

    return {
        "product_id": product["id"],
        "product_title": product["title"],
        "target_dimensions": {"width_px": target_w, "height_px": target_h, "recommended_dpi": rec_dpi, "bleed_mm": bleed_mm},
        "artwork_dimensions": {"width_px": image_width_px, "height_px": image_height_px, "declared_dpi": declared_dpi},
        "effective_dpi": effective_dpi,
        "print_quality_grade": status,
        "is_print_ready": effective_dpi >= 200,
        "bleed_compliance": bleed_mm > 0,
        "scaling_factor": round(effective_scale, 3),
        "feedback": feedback
    }


def audit_artwork_dimensions(
    product_id: Any,
    width_px: int,
    height_px: int,
    file_name: str = "design.png",
    file_size_bytes: Optional[int] = None
) -> Dict[str, Any]:
    """Convenience auditor for CLI and REST endpoints."""
    res = audit_artwork(product_id=product_id, image_width_px=width_px, image_height_px=height_px)
    res["file_name"] = file_name
    if file_size_bytes:
        res["file_size_mb"] = round(file_size_bytes / (1024 * 1024), 2)
    return res
