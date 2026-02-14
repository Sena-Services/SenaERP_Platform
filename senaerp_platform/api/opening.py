# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

"""
Job Opening API
APIs for managing and retrieving job openings
"""

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_active_openings(department=None):
	"""
	Get active job openings (guest accessible)

	Args:
		department (str): Filter by department (optional)

	Returns:
		dict: Success status and openings data

	Example:
		POST /api/method/sentra_core.api.opening.get_active_openings
		Payload: {"department": "Engineering"}
	"""
	try:
		# Build filters
		filters = {"is_active": 1}
		if department:
			filters["department"] = department

		# Fetch active openings
		openings = frappe.get_all(
			"Job Opening",
			filters=filters,
			fields=[
				"name",
				"title",
				"department",
				"positions_open",
				"experience_required",
				"job_description",
				"posted_date"
			],
			order_by="posted_date desc"
		)

		return {
			"success": True,
			"data": openings,
			"count": len(openings)
		}

	except Exception as e:
		frappe.log_error(f"Error fetching openings: {str(e)}", "Opening API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to fetch job openings")
		}


@frappe.whitelist(allow_guest=True)
def get_opening_by_title(title):
	"""
	Get a single job opening by title (guest accessible)

	Args:
		title (str): Job title

	Returns:
		dict: Success status and opening data

	Example:
		POST /api/method/sentra_core.api.opening.get_opening_by_title
		Payload: {"title": "Fullstack Engineer"}
	"""
	try:
		if not title:
			return {
				"success": False,
				"error": "Title is required"
			}

		# Fetch the opening
		opening = frappe.get_all(
			"Job Opening",
			filters={"title": title, "is_active": 1},
			fields=["*"],
			limit=1
		)

		if not opening:
			return {
				"success": False,
				"error": "Opening not found",
				"message": _("The requested job opening does not exist or is not active")
			}

		return {
			"success": True,
			"data": opening[0]
		}

	except Exception as e:
		frappe.log_error(f"Error fetching opening: {str(e)}", "Opening API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to fetch job opening")
		}


@frappe.whitelist()
def create_opening(title, department=None, positions_open=1, experience_required=None,
				   job_description=None, is_active=1):
	"""
	Create a new job opening (requires authentication)

	Args:
		title (str): Job title (required)
		department (str): Department
		positions_open (int): Number of positions
		experience_required (str): Experience required
		job_description (str): Job description (HTML)
		is_active (int): Active status (0 or 1)

	Returns:
		dict: Success status and created opening data

	Example:
		POST /api/method/sentra_core.api.opening.create_opening
		Payload: {
			"title": "Senior Engineer",
			"department": "Engineering",
			"positions_open": 2,
			"experience_required": "5+ years",
			"is_active": 1
		}
	"""
	try:
		# Check permissions
		if not frappe.has_permission("Job Opening", "create"):
			frappe.throw(_("You don't have permission to create job openings"))

		# Create opening document
		opening = frappe.get_doc({
			"doctype": "Job Opening",
			"title": title,
			"department": department,
			"positions_open": int(positions_open),
			"experience_required": experience_required,
			"job_description": job_description,
			"is_active": int(is_active)
		})

		opening.insert()
		frappe.db.commit()

		return {
			"success": True,
			"data": opening.as_dict(),
			"message": _("Job opening created successfully")
		}

	except Exception as e:
		frappe.log_error(f"Error creating opening: {str(e)}", "Opening API Error")
		frappe.db.rollback()
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to create job opening")
		}


@frappe.whitelist()
def update_opening(title, **kwargs):
	"""
	Update an existing job opening (requires authentication)

	Args:
		title (str): Job title (required)
		**kwargs: Fields to update

	Returns:
		dict: Success status and updated opening data

	Example:
		POST /api/method/sentra_core.api.opening.update_opening
		Payload: {
			"title": "Fullstack Engineer",
			"positions_open": 3,
			"is_active": 1
		}
	"""
	try:
		# Check if opening exists
		if not frappe.db.exists("Job Opening", title):
			return {
				"success": False,
				"error": "Opening not found"
			}

		# Check permissions
		if not frappe.has_permission("Job Opening", "write", title):
			frappe.throw(_("You don't have permission to update this opening"))

		# Get and update opening
		opening = frappe.get_doc("Job Opening", title)

		# Update allowed fields
		allowed_fields = ["department", "positions_open", "experience_required",
						  "job_description", "is_active", "posted_date"]
		for field, value in kwargs.items():
			if field in allowed_fields:
				opening.set(field, value)

		opening.save()
		frappe.db.commit()

		return {
			"success": True,
			"data": opening.as_dict(),
			"message": _("Job opening updated successfully")
		}

	except Exception as e:
		frappe.log_error(f"Error updating opening: {str(e)}", "Opening API Error")
		frappe.db.rollback()
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to update job opening")
		}
