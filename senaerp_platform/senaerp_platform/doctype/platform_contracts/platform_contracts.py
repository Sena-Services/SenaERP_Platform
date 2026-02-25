# Copyright (c) 2025, Sena Services and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PlatformContracts(Document):
    """
    Platform Contracts stores contracts synced from external Builder Contract doctypes.

    Contracts are linked to a Provisioned Site based on matching the source site URL.
    This doctype serves as a read-only mirror of contracts created in client sites.
    """

    def before_insert(self):
        """Ensure contract_name is unique."""
        if self.contract_name:
            existing = frappe.db.exists("Platform Contracts", {"contract_name": self.contract_name})
            if existing:
                frappe.throw(f"A contract with ID {self.contract_name} already exists")

    @staticmethod
    def sync_from_builder_contract(contract_data: dict, site_url: str) -> "PlatformContracts":
        """
        Create or update a Platform Contract from Builder Contract data.

        Args:
            contract_data: Dictionary containing Builder Contract fields
            site_url: The site URL to match against Provisioned Site records

        Returns:
            The created or updated Platform Contracts document
        """
        # Find the Provisioned Site by matching site_url
        provisioned_site = frappe.db.get_value(
            "Provisioned Site",
            {"site_url": site_url},
            "name"
        )

        if not provisioned_site:
            # Try matching with trailing slash variations
            site_url_clean = site_url.rstrip("/")
            provisioned_site = frappe.db.get_value(
                "Provisioned Site",
                {"site_url": ["like", f"%{site_url_clean}%"]},
                "name"
            )

        contract_name = contract_data.get("name") or contract_data.get("contract_name")
        if not contract_name:
            frappe.throw("Contract name/ID is required")

        # Check if contract already exists
        existing = frappe.db.get_value(
            "Platform Contracts",
            {"contract_name": contract_name},
            "name"
        )

        if existing:
            doc = frappe.get_doc("Platform Contracts", existing)
        else:
            doc = frappe.new_doc("Platform Contracts")
            doc.contract_name = contract_name

        # Map fields from Builder Contract
        field_mapping = {
            "title": "title",
            "status": "status",
            "builder_mode": "builder_mode",
            "instance": "instance",
            "total_cost": "total_cost",
            "currency": "currency",
            "items_total": "items_total",
            "items_completed": "items_completed",
            "registry_subtotal": "registry_subtotal",
            "builder_subtotal": "builder_subtotal",
            "community_subtotal": "community_subtotal",
            "created_at": "creation",
            "approved_at": "approved_at",
            "build_started_at": "build_started_at",
            "build_completed_at": "build_completed_at",
            "approved_by": "approved_by",
            "rejection_reason": "rejection_reason",
            "build_error": "build_error",
            "notes_content": "notes_content",
            "brd_content": "brd_content",
            "contract_json": "contract_json",
            "terms": "terms",
            "items_json": "items_json",
        }

        for target_field, source_field in field_mapping.items():
            if source_field in contract_data:
                setattr(doc, target_field, contract_data[source_field])

        # Link to Provisioned Site if found
        if provisioned_site:
            doc.provisioned_site = provisioned_site

        doc.save(ignore_permissions=True)
        return doc
