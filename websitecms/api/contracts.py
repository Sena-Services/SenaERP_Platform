# Copyright (c) 2025, Sena Services and contributors
# For license information, please see license.txt

"""
API endpoints for Platform Contracts sync.

These endpoints allow external systems (like sena-agents-backend) to sync
Builder Contracts to the Platform Contracts doctype.
"""

import frappe
import json


@frappe.whitelist(allow_guest=True)
def sync_contract(contract_data: str | dict, site_url: str) -> dict:
    """
    Sync a Builder Contract to Platform Contracts.

    This endpoint receives contract data from an external system and creates
    or updates the corresponding Platform Contracts record, linking it to
    the appropriate Provisioned Site based on the site_url.

    Args:
        contract_data: JSON string or dict containing Builder Contract fields
        site_url: The site URL to match against Provisioned Site records

    Returns:
        dict with success status and the Platform Contracts document name
    """
    if isinstance(contract_data, str):
        contract_data = json.loads(contract_data)

    if not contract_data:
        frappe.throw("contract_data is required")

    if not site_url:
        frappe.throw("site_url is required")

    from websitecms.senaerp_platform.doctype.platform_contracts.platform_contracts import (
        PlatformContracts,
    )

    doc = PlatformContracts.sync_from_builder_contract(contract_data, site_url)

    return {
        "success": True,
        "name": doc.name,
        "contract_name": doc.contract_name,
        "provisioned_site": doc.provisioned_site,
    }


@frappe.whitelist(allow_guest=False)
def get_contracts_for_site(site_url: str) -> list:
    """
    Get all Platform Contracts for a given site URL.

    Args:
        site_url: The site URL to match against Provisioned Site records

    Returns:
        List of Platform Contracts records
    """
    # Find the Provisioned Site
    provisioned_site = frappe.db.get_value(
        "Provisioned Site",
        {"site_url": site_url},
        "name"
    )

    if not provisioned_site:
        site_url_clean = site_url.rstrip("/")
        provisioned_site = frappe.db.get_value(
            "Provisioned Site",
            {"site_url": ["like", f"%{site_url_clean}%"]},
            "name"
        )

    if not provisioned_site:
        return []

    contracts = frappe.get_all(
        "Platform Contracts",
        filters={"provisioned_site": provisioned_site},
        fields=["name", "contract_name", "title", "status", "total_cost", "created_at"],
        order_by="creation desc"
    )

    return contracts


@frappe.whitelist(allow_guest=False)
def delete_contract(contract_name: str) -> dict:
    """
    Delete a Platform Contract by its contract_name (Builder Contract ID).

    Args:
        contract_name: The Builder Contract document name/ID

    Returns:
        dict with success status
    """
    existing = frappe.db.get_value(
        "Platform Contracts",
        {"contract_name": contract_name},
        "name"
    )

    if not existing:
        frappe.throw(f"Contract with ID {contract_name} not found")

    frappe.delete_doc("Platform Contracts", existing, ignore_permissions=True)

    return {"success": True, "deleted": contract_name}
