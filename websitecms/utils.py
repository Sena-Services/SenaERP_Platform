# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

"""
Utility functions for Website CMS
"""

import frappe


def after_request(response):
	"""
	Add CORS headers and cache headers to responses
	Reads configuration from site_config.json
	"""
	# Add cache headers for static files (videos, images, etc.)
	request_path = frappe.request.path if hasattr(frappe, 'request') else ''
	if request_path and request_path.startswith('/files/'):
		# Get file extension
		ext = request_path.lower().split('.')[-1] if '.' in request_path else ''

		# Cache media files aggressively
		if ext in ['mp4', 'webm', 'ogg', 'mov', 'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'pdf']:
			# Cache for 1 year (immutable files)
			response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
			response.headers['Expires'] = frappe.utils.now_datetime() + frappe.utils.timedelta(days=365)
		elif ext in ['js', 'css']:
			# Cache JS/CSS for 1 day
			response.headers['Cache-Control'] = 'public, max-age=86400'

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
