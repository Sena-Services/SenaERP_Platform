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


@frappe.whitelist(allow_guest=True, methods=['POST'])
def add_whatsapp_phone_to_site(phone_number_id: str, display_phone_number: str = None, label: str = None, site_url: str = None):
    """
    Add a WhatsApp phone ID to the Provisioned Site matching the site_url or frontend_site_url.

    This is called after successful WhatsApp Embedded Signup to register the phone
    with the user's provisioned site for webhook routing.

    Args:
        phone_number_id: The WhatsApp phone number ID from Meta
        display_phone_number: The display phone number (e.g., +1 234 567 8900)
        label: Optional label for this phone number (e.g., "Main", "Support")
        site_url: The site URL to match against (frontend_site_url or site_url in Provisioned Site)

    Returns:
        dict with success status and message
    """
    try:
        if not phone_number_id:
            return {"success": False, "message": "phone_number_id is required"}

        if not site_url:
            return {"success": False, "message": "site_url is required"}

        # Normalize the URL for matching (remove trailing slash)
        normalized_url = site_url.rstrip('/')
        print(f"📱 Looking for Provisioned Site matching URL: {normalized_url}")

        # Try to find Provisioned Site matching frontend_site_url first
        provisioned_sites = frappe.get_all(
            "Provisioned Site",
            filters={"frontend_site_url": ["like", f"%{normalized_url}%"]},
            fields=["name", "company_name", "frontend_site_url", "site_url"]
        )

        # If not found by frontend_site_url, try matching by site_url (backend URL)
        if not provisioned_sites:
            print(f"📱 No match on frontend_site_url, trying site_url...")
            provisioned_sites = frappe.get_all(
                "Provisioned Site",
                filters={"site_url": ["like", f"%{normalized_url}%"]},
                fields=["name", "company_name", "frontend_site_url", "site_url"]
            )

        if not provisioned_sites:
            # Log for debugging
            frappe.log_error(
                title="WhatsApp Phone Registration - No Site Found",
                message=f"Site URL: {site_url}\nPhone ID: {phone_number_id}"
            )
            return {
                "success": False,
                "message": f"No Provisioned Site found for URL: {site_url}"
            }

        site = provisioned_sites[0]
        site_doc = frappe.get_doc("Provisioned Site", site.name)

        # Check if this phone_number_id already exists in the child table
        existing_phone = None
        for phone in site_doc.whatsapp_phone_ids:
            if phone.phone_number_id == phone_number_id:
                existing_phone = phone
                break

        if existing_phone:
            # Update existing entry
            existing_phone.display_phone_number = display_phone_number or existing_phone.display_phone_number
            existing_phone.label = label or existing_phone.label
            site_doc.save(ignore_permissions=True)
            frappe.db.commit()

            return {
                "success": True,
                "message": f"WhatsApp phone updated for {site.company_name}",
                "data": {
                    "site_name": site.name,
                    "company_name": site.company_name,
                    "phone_number_id": phone_number_id,
                    "display_phone_number": display_phone_number,
                    "action": "updated"
                }
            }

        # Add new phone to child table
        site_doc.append("whatsapp_phone_ids", {
            "phone_number_id": phone_number_id,
            "display_phone_number": display_phone_number or "",
            "label": label or "Primary"
        })

        site_doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Log success
        frappe.log_error(
            title="WhatsApp Phone Registration Success",
            message=f"Site: {site.company_name}\nSite URL: {site_url}\nPhone ID: {phone_number_id}\nDisplay: {display_phone_number}"
        )

        return {
            "success": True,
            "message": f"WhatsApp phone added to {site.company_name}",
            "data": {
                "site_name": site.name,
                "company_name": site.company_name,
                "phone_number_id": phone_number_id,
                "display_phone_number": display_phone_number,
                "action": "added"
            }
        }

    except Exception as e:
        import traceback
        frappe.log_error(
            title="WhatsApp Phone Registration Error",
            message=f"Error: {str(e)}\n{traceback.format_exc()[:1000]}"
        )
        return {
            "success": False,
            "message": str(e)
        }
