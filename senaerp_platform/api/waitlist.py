# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

"""
Waitlist API
APIs for managing early access waitlist submissions
"""

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def submit_waitlist(full_name, email, company_name=None, phone=None, message=None, access_type=None):
	"""
	Submit early access waitlist form

	Args:
		full_name (str): Full name of the person (required)
		email (str): Email address (required)
		company_name (str): Company name (optional)
		phone (str): Phone number (optional)
		message (str): Message from the user (optional)
		access_type (str): Type of access requested - 'product' or 'pitchdeck' (optional)

	Returns:
		dict: Success status and message

	Example:
		POST /api/method/senaerp_platform.api.waitlist.submit_waitlist
		Payload: {
			"full_name": "John Doe",
			"email": "john@example.com",
			"company_name": "Acme Inc.",
			"phone": "+1 (555) 000-0000",
			"message": "Tell us about yourself",
			"access_type": "product"
		}
	"""
	try:
		# Validate required fields
		if not full_name or not email:
			return {
				"success": False,
				"error": "Full name and email are required",
				"message": _("Please provide both name and email")
			}

		# Check if email already exists in waitlist
		existing = frappe.db.exists("Waitlist", {"email": email})
		if existing:
			return {
				"success": False,
				"error": "Email already registered",
				"message": _("This email is already on the waitlist")
			}

		# Create waitlist entry
		waitlist_entry = frappe.get_doc({
			"doctype": "Waitlist",
			"full_name": full_name,
			"email": email,
			"company_name": company_name or "",
			"phone": phone or "",
			"message": message or "",
			"access_type": access_type or "product",
			"status": "Pending"
		})

		waitlist_entry.insert(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"message": _("Thank you! You've been added to the waitlist."),
			"data": {
				"name": waitlist_entry.name,
				"email": email
			}
		}

	except Exception as e:
		frappe.log_error(f"Error submitting waitlist: {str(e)}", "Waitlist API Error")
		frappe.db.rollback()
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to submit. Please try again.")
		}


@frappe.whitelist()
def get_waitlist_entries(status=None, limit=100):
	"""
	Get waitlist entries (requires authentication)

	Args:
		status (str): Filter by status (optional)
		limit (int): Maximum number of entries to return

	Returns:
		dict: Success status and waitlist entries

	Example:
		POST /api/method/senaerp_platform.api.waitlist.get_waitlist_entries
		Payload: {"status": "Pending", "limit": 50}
	"""
	try:
		# Check permissions
		if not frappe.has_permission("Waitlist", "read"):
			frappe.throw(_("You don't have permission to view waitlist entries"))

		# Build filters
		filters = {}
		if status:
			filters["status"] = status

		# Fetch waitlist entries
		entries = frappe.get_all(
			"Waitlist",
			filters=filters,
			fields=["name", "full_name", "email", "company_name", "phone", "status", "submitted_on"],
			order_by="submitted_on desc",
			limit=int(limit) if limit else 100
		)

		return {
			"success": True,
			"data": entries,
			"count": len(entries)
		}

	except Exception as e:
		frappe.log_error(f"Error fetching waitlist: {str(e)}", "Waitlist API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to fetch waitlist entries")
		}


@frappe.whitelist()
def update_waitlist_status(name, status):
	"""
	Update waitlist entry status (requires authentication)

	Args:
		name (str): Waitlist entry name
		status (str): New status

	Returns:
		dict: Success status and message

	Example:
		POST /api/method/senaerp_platform.api.waitlist.update_waitlist_status
		Payload: {"name": "WAIT-00001", "status": "Contacted"}
	"""
	try:
		# Check if entry exists
		if not frappe.db.exists("Waitlist", name):
			return {
				"success": False,
				"error": "Waitlist entry not found"
			}

		# Check permissions
		if not frappe.has_permission("Waitlist", "write", name):
			frappe.throw(_("You don't have permission to update this entry"))

		# Update status
		frappe.db.set_value("Waitlist", name, "status", status)
		frappe.db.commit()

		return {
			"success": True,
			"message": _("Status updated successfully")
		}

	except Exception as e:
		frappe.log_error(f"Error updating waitlist status: {str(e)}", "Waitlist API Error")
		frappe.db.rollback()
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to update status")
		}
