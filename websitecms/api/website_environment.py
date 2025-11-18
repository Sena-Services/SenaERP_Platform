# Copyright (c) 2025, Sena and contributors
# For license information, please see license.txt

"""
Website Environment API
APIs for managing and retrieving environment data for the marketing website
"""

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_published_environments(limit=10, fields=None):
	"""
	Get list of published environments

	Args:
		limit (int): Maximum number of environments to return (default: 10)
		fields (list): List of fields to return (optional)

	Returns:
		dict: Success status and environment data

	Example:
		GET/POST /api/method/websitecms.api.website_environment.get_published_environments
		Payload: {"limit": 10}
	"""
	try:
		# Default fields to return
		if not fields:
			fields = [
				"name",
				"environment_id",
				"label",
				"category",
				"status",
				"persona",
				"summary",
				"interface_count",
				"data_count",
				"workflows_count",
				"agents_count",
				"bullet_1",
				"bullet_2",
				"bullet_3",
				"display_order"
			]

		# Validate limit
		limit = int(limit) if limit else 10
		if limit > 100:
			limit = 100  # Cap at 100 to prevent excessive data transfer

		# Fetch published environments
		environments = frappe.get_all(
			"Website Environment",
			filters={"published": 1},
			fields=fields,
			order_by="display_order asc",
			limit=limit
		)

		# Transform data to match frontend structure
		transformed_environments = []
		for env in environments:
			# Build metrics array
			metrics = [
				{
					"id": "interface",
					"label": "Interface",
					"value": str(env.get("interface_count", 0)),
					"icon": "layout"
				},
				{
					"id": "data",
					"label": "Data",
					"value": str(env.get("data_count", 0)),
					"icon": "database"
				},
				{
					"id": "workflows",
					"label": "Workflows",
					"value": str(env.get("workflows_count", 0)),
					"icon": "zap"
				},
				{
					"id": "agents",
					"label": "Agents",
					"value": str(env.get("agents_count", 0)),
					"icon": "cpu"
				}
			]

			# Build bullets array
			bullets = []
			for i in range(1, 4):
				bullet_field = f"bullet_{i}"
				if env.get(bullet_field):
					bullets.append(env.get(bullet_field))

			# Build blueprint counts
			blueprint_counts = {
				"Interface": env.get("interface_count", 0),
				"Data": env.get("data_count", 0),
				"Workflows": env.get("workflows_count", 0),
				"Agents": env.get("agents_count", 0)
			}

			transformed_env = {
				"id": env.get("environment_id"),
				"label": env.get("label"),
				"category": env.get("category"),
				"persona": env.get("persona"),
				"summary": env.get("summary"),
				"bullets": bullets,
				"metrics": metrics,
				"blueprintCounts": blueprint_counts
			}

			transformed_environments.append(transformed_env)

		return {
			"success": True,
			"data": transformed_environments,
			"count": len(transformed_environments)
		}

	except Exception as e:
		frappe.log_error(f"Error fetching published environments: {str(e)}", "Website Environment API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to fetch environments")
		}


@frappe.whitelist(allow_guest=True)
def get_environment_by_id(environment_id):
	"""
	Get a single environment by environment_id

	Args:
		environment_id (str): Environment ID (e.g., 'travel-agency')

	Returns:
		dict: Success status and environment data

	Example:
		GET/POST /api/method/websitecms.api.website_environment.get_environment_by_id
		Payload: {"environment_id": "travel-agency"}
	"""
	try:
		if not environment_id:
			return {
				"success": False,
				"error": "environment_id must be provided"
			}

		environments = frappe.get_all(
			"Website Environment",
			filters={"published": 1, "environment_id": environment_id},
			fields=["*"],
			limit=1
		)

		if not environments:
			return {
				"success": False,
				"error": "Environment not found",
				"message": _("The requested environment does not exist or is not published")
			}

		env = environments[0]

		# Transform to match frontend structure
		metrics = [
			{
				"id": "interface",
				"label": "Interface",
				"value": str(env.get("interface_count", 0)),
				"icon": "layout"
			},
			{
				"id": "data",
				"label": "Data",
				"value": str(env.get("data_count", 0)),
				"icon": "database"
			},
			{
				"id": "workflows",
				"label": "Workflows",
				"value": str(env.get("workflows_count", 0)),
				"icon": "zap"
			},
			{
				"id": "agents",
				"label": "Agents",
				"value": str(env.get("agents_count", 0)),
				"icon": "cpu"
			}
		]

		bullets = []
		for i in range(1, 4):
			bullet_field = f"bullet_{i}"
			if env.get(bullet_field):
				bullets.append(env.get(bullet_field))

		blueprint_counts = {
			"Interface": env.get("interface_count", 0),
			"Data": env.get("data_count", 0),
			"Workflows": env.get("workflows_count", 0),
			"Agents": env.get("agents_count", 0)
		}

		transformed_env = {
			"id": env.get("environment_id"),
			"label": env.get("label"),
			"category": env.get("category"),
			"persona": env.get("persona"),
			"summary": env.get("summary"),
			"bullets": bullets,
			"metrics": metrics,
			"blueprintCounts": blueprint_counts
		}

		return {
			"success": True,
			"data": transformed_env
		}

	except Exception as e:
		frappe.log_error(f"Error fetching environment by ID: {str(e)}", "Website Environment API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to fetch environment")
		}


@frappe.whitelist(allow_guest=True)
def get_environment_count():
	"""
	Get count of published environments

	Returns:
		dict: Success status and count

	Example:
		GET/POST /api/method/websitecms.api.website_environment.get_environment_count
	"""
	try:
		count = frappe.db.count("Website Environment", filters={"published": 1})

		return {
			"success": True,
			"count": count
		}

	except Exception as e:
		frappe.log_error(f"Error getting environment count: {str(e)}", "Website Environment API Error")
		return {
			"success": False,
			"error": str(e),
			"message": _("Failed to get environment count")
		}
