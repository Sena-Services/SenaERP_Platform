# Copyright (c) 2025, Sena and contributors
# For license information, please see license.txt

"""Registry API endpoints.

List, search, and fetch registry items (agents, teams, tools, UI, code).
"""

from __future__ import annotations

import json
from typing import Any

import frappe


@frappe.whitelist(allow_guest=True)
def list_registry_items(
    item_type: str | None = None,
    category: str | None = None,
    enabled_only: bool = True,
) -> list[dict[str, Any]]:
    """List registry items with optional filtering.

    GET /api/method/senaerp_platform.api.registry.list_registry_items
    """
    filters: dict[str, Any] = {}

    if bool(int(enabled_only)) if isinstance(enabled_only, str) else enabled_only:
        filters["enabled"] = 1

    if item_type:
        filters["item_type"] = item_type

    if category:
        filters["category"] = category

    rows = frappe.get_all(
        "Registry Item",
        filters=filters,
        fields=[
            "name",
            "item_type",
            "title",
            "description",
            "category",
            "tags",
            "dotmatrix_avatar",
            "enabled",
            "installed",
            "install_count",
            "author",
            "version",
        ],
        order_by="title asc",
    )

    return [
        {
            **r,
            "enabled": bool(r.enabled),
            "installed": bool(r.installed),
            "tags": _parse_json(r.tags),
        }
        for r in rows
    ]


@frappe.whitelist(allow_guest=True)
def get_registry_item(name: str) -> dict[str, Any]:
    """Get a single registry item with full details including payload.

    GET /api/method/senaerp_platform.api.registry.get_registry_item
    """
    if not name:
        frappe.throw("name is required")

    if not frappe.db.exists("Registry Item", name):
        frappe.throw(f"Registry item '{name}' not found")

    doc = frappe.get_cached_doc("Registry Item", name)

    return {
        "name": doc.name,
        "item_type": doc.item_type,
        "title": doc.title,
        "description": doc.description,
        "category": doc.category,
        "tags": _parse_json(doc.tags),
        "dotmatrix_avatar": doc.dotmatrix_avatar,
        "enabled": bool(doc.enabled),
        "installed": bool(doc.installed),
        "install_count": doc.install_count or 0,
        "author": doc.author,
        "version": doc.version,
        "source_url": doc.source_url,
        "payload": _parse_json(doc.payload),
    }


@frappe.whitelist(allow_guest=True)
def search_registry(
    query: str,
    item_type: str | None = None,
) -> list[dict[str, Any]]:
    """Search registry items by title or description.

    GET /api/method/senaerp_platform.api.registry.search_registry
    """
    if not query or len(query.strip()) < 2:
        frappe.throw("Search query must be at least 2 characters")

    query = query.strip()

    filters: dict[str, Any] = {"enabled": 1}
    if item_type:
        filters["item_type"] = item_type

    or_filters = [
        ["title", "like", f"%{query}%"],
        ["description", "like", f"%{query}%"],
        ["category", "like", f"%{query}%"],
        ["tags", "like", f"%{query}%"],
    ]

    rows = frappe.get_all(
        "Registry Item",
        filters=filters,
        or_filters=or_filters,
        fields=[
            "name",
            "item_type",
            "title",
            "description",
            "category",
            "tags",
            "dotmatrix_avatar",
            "installed",
            "install_count",
            "author",
        ],
        order_by="install_count desc, title asc",
        limit_page_length=50,
    )

    return [
        {
            **r,
            "installed": bool(r.installed),
            "tags": _parse_json(r.tags),
        }
        for r in rows
    ]


def _parse_json(value: Any) -> Any:
    """Parse a JSON string field, returning empty list/dict on failure."""
    if not value:
        return []
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []
