# Copyright (c) 2025, Sentra and contributors
# For license information, please see license.txt

"""
Authentication endpoints for Website CMS Landing Page
Validates company credentials against Provisioned Site records
"""

import frappe
from frappe import _
from frappe.utils import now_datetime, add_to_date
import secrets


@frappe.whitelist(allow_guest=True)
def login(email=None, password=None):
	"""
	Login for provisioned site companies
	Validates credentials against Provisioned Site doctype
	Returns site URL for redirect and auto-login

	Args:
		email (str): Company email address
		password (str): Administrator password for their site

	Returns:
		dict: Success status, site_url, and company details
	"""
	try:
		if not email or not password:
			return {
				"success": False,
				"error": _("Email and password are required")
			}

		# Find provisioned site by email
		provisioned_sites = frappe.get_all(
			"Provisioned Site",
			filters={"email": email, "status": "Active"},
			fields=["name", "company_name", "email", "site_url", "administrator_password"]
		)

		if not provisioned_sites:
			return {
				"success": False,
				"error": _("Invalid email or password")
			}

		site = provisioned_sites[0]

		# Verify password
		# Note: Frappe Password fields are stored encrypted, need to use get_password
		stored_password = frappe.utils.password.get_decrypted_password(
			"Provisioned Site",
			site.name,
			"administrator_password"
		)

		if stored_password != password:
			return {
				"success": False,
				"error": _("Invalid email or password")
			}

		# Generate one-time login token
		token = secrets.token_urlsafe(32)
		expires_at = add_to_date(now_datetime(), minutes=5)

		# Create Login Token record
		login_token = frappe.get_doc({
			"doctype": "Login Token",
			"token": token,
			"email": site.email,
			"site_url": site.site_url,
			"administrator_password": stored_password,
			"used": 0,
			"expires_at": expires_at
		})
		login_token.insert(ignore_permissions=True)
		frappe.db.commit()

		# Return token and site URL for redirect
		return {
			"success": True,
			"message": _("Login successful"),
			"site_url": site.site_url,
			"token": token,
			"company_name": site.company_name
		}

	except Exception as e:
		frappe.log_error(f"Login error: {str(e)}", "Landing Page Login Error")
		return {
			"success": False,
			"error": _("Login failed. Please try again.")
		}


@frappe.whitelist(allow_guest=True)
def validate_token(token=None):
	"""
	Validate and consume a one-time login token
	Called by provisioned sites to authenticate users

	Args:
		token (str): The one-time login token

	Returns:
		dict: Success status and administrator password if valid
	"""
	try:
		if not token:
			return {
				"success": False,
				"error": _("Token is required")
			}

		# Find the token
		login_tokens = frappe.get_all(
			"Login Token",
			filters={"token": token},
			fields=["name", "used", "expires_at", "email", "site_url", "administrator_password"]
		)

		if not login_tokens:
			return {
				"success": False,
				"error": _("Invalid token")
			}

		token_doc = login_tokens[0]

		# Check if already used
		if token_doc.used:
			return {
				"success": False,
				"error": _("Token already used")
			}

		# Check if expired
		if now_datetime() > token_doc.expires_at:
			return {
				"success": False,
				"error": _("Token expired")
			}

		# Mark token as used
		frappe.db.set_value("Login Token", token_doc.name, "used", 1)
		frappe.db.commit()

		return {
			"success": True,
			"email": token_doc.email,
			"site_url": token_doc.site_url
		}

	except Exception as e:
		frappe.log_error(f"Token validation error: {str(e)}", "Token Validation Error")
		return {
			"success": False,
			"error": _("Token validation failed")
		}


@frappe.whitelist(allow_guest=True)
def validate_session():
	"""
	Check if current session is valid
	For landing page, this just checks if user has an active Frappe session
	"""
	try:
		if frappe.session.user and frappe.session.user != "Guest":
			return {
				"valid": True,
				"user": frappe.session.user,
				"session_status": "active"
			}
		return {
			"valid": False,
			"user": None,
			"session_status": "guest"
		}
	except Exception as e:
		return {
			"valid": False,
			"error": str(e),
			"session_status": "error"
		}


@frappe.whitelist(allow_guest=True)
def get_current_user():
	"""
	Get current logged-in user for the landing page
	Called by Next.js environment selector to check authentication

	Landing page users are always Administrator (logged in via auto_login_from_provisioned)
	This endpoint just confirms authentication status

	Returns:
		dict: Success status and minimal user info
	"""
	try:
		# Check if user is logged in
		if frappe.session.user == "Guest":
			return {
				"success": False,
				"user": None,
				"is_guest": True
			}

		# User is authenticated (always Administrator on landing page)
		return {
			"success": True,
			"user": {
				"email": frappe.session.user,
				"full_name": "Administrator",
				"first_name": "Admin",
				"last_name": "",
				"user_type": "System User"
			}
		}

	except Exception as e:
		frappe.log_error(f"Get current user error: {str(e)}", "Get Current User Error")
		return {
			"success": False,
			"user": None,
			"error": str(e)
		}


@frappe.whitelist()
def logout():
	"""
	Logout the current user from the landing page
	Called by Next.js when user wants to logout

	Returns:
		dict: Success status
	"""
	try:
		frappe.local.login_manager.logout()
		frappe.db.commit()

		return {
			"success": True,
			"message": _("Logged out successfully")
		}
	except Exception as e:
		frappe.log_error(f"Logout error: {str(e)}", "Logout Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def get_user_site_url():
	"""
	Get the provisioned site URL for the currently logged-in user
	Reads from session data which was stored during auto_login_from_provisioned

	Each Administrator session on the landing page represents a different provisioned site
	The session data tracks which site each session belongs to

	Returns:
		dict: Success status and site_url
	"""
	import json

	try:
		# Check if user is logged in
		if frappe.session.user == "Guest":
			return {
				"success": False,
				"error": _("Not logged in")
			}

		# Get session data from database (use SQL since Sessions table doesn't have 'name' column)
		session_data = frappe.db.sql("""
			SELECT sessiondata
			FROM `tabSessions`
			WHERE sid = %s
		""", (frappe.session.sid,))

		if not session_data or not session_data[0][0]:
			return {
				"success": False,
				"error": _("Session data not found")
			}

		session_data = session_data[0][0]

		# Parse session data to get provisioned site URL
		session_info = json.loads(session_data)
		provisioned_site_url = session_info.get("provisioned_site_url")

		if not provisioned_site_url:
			return {
				"success": False,
				"error": _("Provisioned site URL not found in session")
			}

		return {
			"success": True,
			"site_url": provisioned_site_url
		}

	except Exception as e:
		frappe.log_error(f"Get user site URL error: {str(e)}", "Get User Site URL Error")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist(allow_guest=True)
def auto_login(token=None):
	"""
	Auto-login using one-time token from landing page
	Validates token and logs user into their provisioned site

	Args:
		token (str): One-time login token

	Returns:
		Redirects to site home on success, or returns error
	"""
	try:
		if not token:
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = "/login?error=missing_token"
			return

		# Validate token directly (no cross-site request needed)
		validation_result = validate_token(token)

		if not validation_result.get("success"):
			error = validation_result.get("error", "invalid_token").lower().replace(" ", "_")
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = f"/login?error={error}"
			return

		# Get site URL from validation response
		site_url = validation_result["site_url"]

		# Login as Administrator (token already validated)
		frappe.local.login_manager.login_as("Administrator")

		# Commit the session to database (required for GET requests)
		frappe.db.commit()

		# Redirect to the provisioned site frontend
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = site_url

	except Exception as e:
		frappe.log_error(f"Auto-login error: {str(e)}", "Auto-login Error")
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = "/login?error=unexpected"
		return


@frappe.whitelist(allow_guest=True)
def create_landing_token_for_site(site_url=None):
	"""
	Create a login token for a provisioned site user to access the landing page
	This is the reverse of the normal login flow - allows users to go from
	provisioned site → landing page (for environment selector)

	Args:
		site_url (str): The provisioned site URL

	Returns:
		dict: Success status and token if valid
	"""
	try:
		if not site_url:
			return {
				"success": False,
				"error": _("Site URL is required")
			}

		# Find provisioned site by site_url or frontend URL
		provisioned_sites = frappe.get_all(
			"Provisioned Site",
			filters={
				"status": "Active"
			},
			fields=["name", "company_name", "email", "site_url"]
		)

		# Match by site_url (could be the frontend_url)
		matching_site = None
		for site in provisioned_sites:
			# Check if the provided URL matches the site_url or is part of it
			if site_url in site.site_url or site.site_url in site_url:
				matching_site = site
				break

		if not matching_site:
			frappe.log_error(f"No provisioned site found for URL: {site_url}", "Landing Token Error")
			return {
				"success": False,
				"error": _("Site not found")
			}

		# Generate one-time login token for landing page
		token = secrets.token_urlsafe(32)
		expires_at = add_to_date(now_datetime(), minutes=5)

		# Create Login Token record
		# Note: administrator_password is not needed for reverse flow (provisioned → landing)
		# but the field exists in the doctype so we set it to empty string
		login_token = frappe.get_doc({
			"doctype": "Login Token",
			"token": token,
			"email": matching_site.email,
			"site_url": matching_site.site_url,
			"administrator_password": "",
			"used": 0,
			"expires_at": expires_at
		})
		login_token.insert(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"token": token,
			"email": matching_site.email
		}

	except Exception as e:
		frappe.log_error(f"Create landing token error: {str(e)}", "Landing Token Error")
		return {
			"success": False,
			"error": _("Failed to create token")
		}


@frappe.whitelist(allow_guest=True)
def auto_login_from_provisioned(token=None, redirect_to=None):
	"""
	Auto-login to landing page using token from provisioned site
	This creates a session on the landing page so users can access environment selector

	Args:
		token (str): One-time login token created by provisioned site
		redirect_to (str): Optional path to redirect to after login (default: /environment-selector)

	Returns:
		Redirects to environment selector or specified page
	"""
	try:
		if not token:
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = "/login?error=missing_token"
			return

		# Validate token
		validation_result = validate_token(token)

		if not validation_result.get("success"):
			error = validation_result.get("error", "invalid_token").lower().replace(" ", "_")
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = f"/login?error={error}"
			return

		# Login as Administrator on the landing page
		# This creates a session cookie on the landing page domain
		frappe.local.login_manager.login_as("Administrator")

		# Store the provisioned site email and URL in session data
		# This allows us to identify which provisioned site this session belongs to
		# Each session is independent, so multiple sites can be logged in simultaneously
		email = validation_result.get("email")
		site_url = validation_result.get("site_url")

		# Update session data in database (Sessions table uses sid, not name)
		frappe.db.sql("""
			UPDATE `tabSessions`
			SET sessiondata = %s
			WHERE sid = %s
		""", (frappe.as_json({
			"provisioned_site_email": email,
			"provisioned_site_url": site_url
		}), frappe.session.sid))

		# Commit the session to database
		frappe.db.commit()

		# Redirect to environment selector or specified page
		# Use relative path since we're already on the landing page domain
		redirect_path = redirect_to or "/environment-selector"
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = redirect_path

	except Exception as e:
		frappe.log_error(f"Auto-login from provisioned error: {str(e)}", "Auto-login Error")
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = "/login?error=unexpected"
		return
