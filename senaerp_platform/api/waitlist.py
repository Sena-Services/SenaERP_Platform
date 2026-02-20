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

		# Check if email already exists in waitlist for this access type
		existing = frappe.db.exists("Waitlist", {"email": email, "access_type": access_type or "Product"})
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
			"access_type": access_type or "Product",
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


@frappe.whitelist()
def sync_contract(user_email, contract_data):
	"""
	Sync a contract from sena-agents-backend to the Waitlist.
	Called by the Builder Contract doctype when a contract is created or updated.

	Args:
		user_email (str): Email of the user who created the contract
		contract_data (dict): Contract data to sync

	Returns:
		dict: Success status and message

	Example:
		POST /api/method/senaerp_platform.api.waitlist.sync_contract
		Headers: Authorization: token api_key:api_secret
		Payload: {
			"user_email": "user@example.com",
			"contract_data": {
				"contract_name": "BC-00001",
				"title": "My Contract",
				"status": "Draft",
				...
			}
		}
	"""
	try:
		import json

		# Parse contract_data if it's a string
		if isinstance(contract_data, str):
			contract_data = json.loads(contract_data)

		if not user_email:
			return {
				"success": False,
				"error": "user_email is required"
			}

		# Find Waitlist entry matching this email
		waitlist_name = frappe.db.get_value("Waitlist", {"email": user_email}, "name")
		if not waitlist_name:
			return {
				"success": False,
				"error": f"No Waitlist entry found for email: {user_email}"
			}

		waitlist = frappe.get_doc("Waitlist", waitlist_name)

		# Check if contract already exists in waitlist
		existing_row = None
		contract_name = contract_data.get("contract_name")
		for row in waitlist.contracts or []:
			if row.contract_name == contract_name:
				existing_row = row
				break

		if existing_row:
			# Update existing row
			for key, value in contract_data.items():
				if hasattr(existing_row, key):
					setattr(existing_row, key, value)
		else:
			# Add new row
			waitlist.append("contracts", contract_data)

		waitlist.flags.ignore_permissions = True
		waitlist.save()
		frappe.db.commit()

		return {
			"success": True,
			"message": f"Contract {contract_name} synced to Waitlist {waitlist_name}",
			"waitlist": waitlist_name
		}

	except Exception as e:
		frappe.log_error(f"Error syncing contract: {str(e)}", "Contract Sync API Error")
		frappe.db.rollback()
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to sync contract")
		}
