"""
WhatsApp Router API

Provides lookup endpoint for the WhatsApp webhook router to find
which site handles a given phone_number_id.
"""

import frappe


@frappe.whitelist(allow_guest=True)
def get_site_for_phone_id(phone_number_id: str):
    """
    Look up which Provisioned Site handles a given WhatsApp phone_number_id.

    Args:
        phone_number_id: The WhatsApp phone number ID from webhook metadata

    Returns:
        dict with site_url if found, or error message if not found
    """
    if not phone_number_id:
        return {"error": "phone_number_id is required"}

    # Query the child table to find which Provisioned Site has this phone_id
    result = frappe.db.sql(
        """
        SELECT ps.site_url, ps.company_name, ps.status
        FROM `tabProvisioned Site` ps
        INNER JOIN `tabWhatsApp Phone ID` wp ON wp.parent = ps.name
        WHERE wp.phone_number_id = %s
        AND ps.status = 'Active'
        LIMIT 1
        """,
        (phone_number_id,),
        as_dict=True
    )

    if result:
        site = result[0]
        return {
            "site_url": site.site_url,
            "company_name": site.company_name,
            "status": site.status
        }

    return {"error": f"No active site found for phone_number_id: {phone_number_id}"}


@frappe.whitelist(allow_guest=True)
def get_all_phone_mappings():
    """
    Get all phone_number_id to site_url mappings.
    Useful for pre-populating the router cache.

    Returns:
        dict with mappings: {phone_number_id: site_url, ...}
    """
    results = frappe.db.sql(
        """
        SELECT wp.phone_number_id, ps.site_url
        FROM `tabProvisioned Site` ps
        INNER JOIN `tabWhatsApp Phone ID` wp ON wp.parent = ps.name
        WHERE ps.status = 'Active'
        """,
        as_dict=True
    )

    mappings = {r.phone_number_id: r.site_url for r in results}
    return {"mappings": mappings, "count": len(mappings)}
