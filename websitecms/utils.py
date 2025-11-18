# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

"""
Utility functions for Website CMS
"""

import frappe


def after_request(response):
	"""
	Add CORS headers to all responses
	Reads configuration from site_config.json
	"""
	# Get CORS config from site_config
	allow_cors = frappe.conf.get("allow_cors")

	if not allow_cors:
		return response

	# Get origin from request
	origin = frappe.get_request_header("Origin")

	# Handle multiple allowed origins
	allowed_origins = []
	if isinstance(allow_cors, list):
		allowed_origins = allow_cors
	elif isinstance(allow_cors, str):
		if allow_cors == "*":
			allowed_origins = ["*"]
		else:
			allowed_origins = [allow_cors]

	# Check if origin is allowed
	if origin:
		if "*" in allowed_origins or origin in allowed_origins:
			response.headers["Access-Control-Allow-Origin"] = origin

			# Add credentials header if configured
			if frappe.conf.get("cors_allow_credentials"):
				response.headers["Access-Control-Allow-Credentials"] = "true"

			# Add allowed methods
			allow_methods = frappe.conf.get("allow_cors_methods", "GET,POST,PUT,DELETE,OPTIONS")
			response.headers["Access-Control-Allow-Methods"] = allow_methods

			# Add allowed headers
			allow_headers = frappe.conf.get(
				"allow_cors_headers",
				"Content-Type,Authorization,X-Frappe-CSRF-Token,Accept"
			)
			response.headers["Access-Control-Allow-Headers"] = allow_headers

			# Add max age for preflight requests
			response.headers["Access-Control-Max-Age"] = "86400"  # 24 hours

			# Expose headers for JavaScript access
			response.headers["Access-Control-Expose-Headers"] = "Set-Cookie"

	return response
